#%%
import json
import os
import pandas as pd
import numpy as np
#display all columns
pd.set_option('display.max_columns', None)

import shutil

from Bio.PDB import PDBParser
p = PDBParser(QUIET=True)

from scipy.spatial.distance import euclidean
import scipy.cluster.hierarchy as sch

from pwes.plotting.plotting import plot_PWES_method

class PWES_for_protein:
    def __init__(self, pdb_name, pdb_path, chain="A", output_dir = "./figures", protein_name =None, output_suffix ='', data_path=None, data_sep = "\t", input_df=None):
        """
        
        Constructor for the PWES_for_protein class
        
        args:
        
        pdb_name: str, name of the pdb file
        pdb_path: str, path to the pdb file
        chain: str, chain of the protein
        output_dir: str, path to the output directory
        protein_name: str, name of the protein
        suffix: str, suffix for the output directory
        data_path: str, path to the data file
        data_sep: str, separator for the data file
        input_df: pandas DataFrame, input data frame
        
        Called methods:
        get_df: get the data frame from the data file
        get_structure: get the structure of the protein
        
        """
        
        # define attributes relating to naming and pdb file
        self.pdb_name = pdb_name
        self.pdb_path = pdb_path
        self.chain = chain
        if protein_name is None:
            self.protein_name = self.pdb_name
        else:
            self.protein_name = protein_name
        
        self.suffix = output_suffix
        
        if not self.pdb_path[-4:] == ".pdb":
            self.pdb_location = f"{self.pdb_path}/{self.pdb_name}.pdb"
        
        try:
            self.structure = self.get_structure()
        except:
            raise Exception("PDB file not found")
        
        
        # handle the input data
        
        assert data_path is not None or input_df is not None, "Either data_path or input_df must be provided"
        
        self.data_path = data_path

        if type(input_df) is pd.DataFrame:
            self.df = input_df
        else:
            try:
                self.data_sep = data_sep
                self.df = self.get_df()
            except:
                raise Exception("Data file not found")
                
        
        
        self.output_dir = os.path.join(output_dir, self.protein_name, self.suffix)
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        
        
        self.PWES_array, self.dij_array, self.xij_array, self.df, self.linkage_matrix = self.calc_PWES_pwij()
        
        self.n_clusters_computed = []
        
        self.dict_of_scores = {}
        
        
    ############################################################################################################


    def get_structure(self):
        
        
        p = PDBParser(QUIET=True)
        structure = p.get_structure(self.protein_name, f"{self.pdb_path}/{self.pdb_name}.pdb")
        # copy structure to f"figures/{self.protein_name}/{self.suffix}/{self.pdb_name}/"
        shutil.copy(f"{self.pdb_path}/{self.pdb_name}.pdb", f"figures/{self.protein_name}/{self.suffix}/{self.pdb_name}/")
        return structure

    ############################################################################################################

    def get_df(self):
        df = pd.read_csv(self.data_path, sep=self.data_sep, index_col=False)
        return df


    ############################################################################################################

    def calc_PWES_pwij(self):
        
        
        residues_in_pdb = self.structure[0][self.chain].get_residues()
        # remove all het atoms
        resnum_in_pdb = [res.get_id()[1] for res in residues_in_pdb if res.get_id()[0] == " "]

        
        df = self.df.copy()
        
        
        #remove rows where res_num = []
        df["guide_idx"] = df.index
        df["resnum"] = df["resnum"].str.apply(lambda x: x.split(";"))
        df = df[self.df["resnum"].apply(lambda x: len(x) > 0)]
        
        df = df.reset_index(drop=True)
        
        # remove rows if any res_num is not in the pdb
        df = df[df["resnum"].apply(lambda x: all([int(res_num) in resnum_in_pdb for res_num in x]))]
        df = df.reset_index(drop=True)

        num_rows = df.shape[0]

        xij_array = np.zeros((num_rows, num_rows))
        dij_array = np.zeros((num_rows, num_rows))
        PWES_array = np.zeros((num_rows, num_rows))
        for i, rowi in df.iterrows():
            guidei_atoms_coordinates = []
            for res_num in set(rowi["resnum"]):
                    res = self.structure[0][self.chain][int(res_num)]
                    for atom in res:
                        guidei_atoms_coordinates.append(atom.get_coord())
            
            # turn into numpy array
            guidei_atoms_coordinates = np.array(guidei_atoms_coordinates)
            #calculate centroid
            c1 = np.mean(guidei_atoms_coordinates, axis=0)
            c1 = c1.flatten()
            for j, rowj in df.iterrows():
                
                if i == j:
                    continue
                
                guidej_atoms_coordinates = []
                for res_num in set(rowj["resnum"]):
                    res = self.structure[0][self.chain][int(res_num)]
                    for atom in res:
                        guidej_atoms_coordinates.append(atom.get_coord())
        
                # turn into numpy array
                guidej_atoms_coordinates = np.array(guidej_atoms_coordinates)
                #calculate centroid
                c2 = np.mean(guidej_atoms_coordinates, axis=0)
                # make 1d
                c2 = c2.flatten()
                
                # calculate the euclidean distance between the centroids
                try:
                    dij_array[i,j] = euclidean(c1, c2)
                except:

                    break
                # calculate the xij
                xij_array[i,j] = rowi["lfc"] + rowj["lfc"]

        #calculate mean and std of xij
        xij_mean = np.mean(xij_array)
        xij_std = np.std(xij_array)
    
        t = 16
        #calculate pwij
        for i in range(num_rows):
            for j in range(num_rows):
                pwij = np.tanh((xij_array[i,j] - xij_mean)/xij_std)*np.exp(-((dij_array[i,j]**2)/(2*t**2)))
                PWES_array[i, j] = pwij
        np.fill_diagonal(PWES_array, 0)
        
        linkage_matrix = sch.linkage(PWES_array, method="ward", metric="euclidean")
        

        return PWES_array, dij_array, xij_array, df, linkage_matrix


    ############################################################################################################


    def plot_PWES(self, threshold):
        
        dict_of_clusters, wcss, silhouette_score = plot_PWES_method(self,threshold)
        
        

    # def generate_script_variation(self, directory, n_clusters):
    #     # Read the template script
    #     with open('/Users/gbp326/Library/CloudStorage/OneDrive-UniversityofCopenhagen/Pockedit/wdir/scripts/template_script.py', 'r') as f:
    #         template_code = f.read()

    #     json_file = "clusters.json"

    #     # Replace placeholders with actual values
    #     template_code = template_code.replace('<JSON_FILE>', json_file)
    #     template_code = template_code.replace('<PDB_NAME>', self.pdb_name)
    #     template_code = template_code.replace('<UNIPROT_ID>', self.uniprot_id)
    #     template_code = template_code.replace('<CHAIN>', self.chain)
    #     template_code = template_code.replace('<ACTIVE_SITES>', f"{list(self.ActivEdit_dict.keys()) if self.ActivEdit_dict else None}")

    #     # Write the variation script to file
    #     variation_file = os.path.join(directory, f'{self.pdb_name}_{n_clusters}_ChimeraX.py')
    #     with open(variation_file, 'w') as f:
    #         f.write(template_code)


    # def perform_for_all_thresholds(self):
        
    #     if os.path.exists(f"figures/{self.protein_name}/{self.suffix}/{self.pdb_name}/WCSS_vs_Clusters.pdf"):
    #         print(f"Already performed for {self.protein_name} {self.suffix} {self.pdb_name}")
    #         return None
        
    #     thresholds = list(np.linspace(4, 30, 53))
    #     for threshold in thresholds:
            
    #         cluster_dict, wcss, silhouette_score = self.plot_PWES(threshold)
    #         if len(cluster_dict) == 0 or len(cluster_dict) > 50:
    #             continue
    #         if len(cluster_dict) not in self.dict_of_scores:
    #             self.dict_of_scores[len(cluster_dict)] = {"clusters": cluster_dict, "wcss": wcss, "silhouette_score": silhouette_score, "threshold": threshold}
        
    #     with open(f"figures/{self.protein_name}/{self.suffix}/{self.pdb_name}/scores.json", "w") as f:
    #         json.dump(self.dict_of_scores, f)
        
        
    #     ##### plotting 
        
    #     #plot the wcss and silhouette score
    #     # get list of keys as integers and sort them
    #     keys = [int(key) for key in self.dict_of_scores.keys()]
    #     keys.sort()
    #     # plot the wcss and silhouette score
    #     wcss = [self.dict_of_scores[key]["wcss"] for key in keys]
    #     silhouette_score = [self.dict_of_scores[key]["silhouette_score"] for key in keys]
    #     plt.plot(keys, wcss)
    #     plt.xlabel("Number of Clusters")
    #     plt.ylabel("WCSS")
    #     plt.title(f"Gene: {self.protein_name}\nWCSS vs Number of Clusters")
    #     plt.savefig(f"figures/{self.protein_name}/{self.suffix}/{self.pdb_name}/WCSS_vs_Clusters.pdf")
    #     plt.close()
        
        
        
    #     ##### simulate pwes for 3 highest silhouette scores and 3 highest alt silhouette scores
        
    #     ### simulate pwes for 3 highest silhouette scores
    #     #find the 3 highest silhouette scores
    #     silhouette_scores = [self.dict_of_scores[key]["silhouette_score"] for key in keys]
    #     # alt_silhouette_scores = [self.dict_of_scores[key]["alt_silhouette"] for key in keys]
    #     # get the indices of the clusters with 10 to 30 clusters
    #     valid_indices = [i for i, key in enumerate(keys) if 10 <= key <= 30]
    #     # get the silhouette scores and alt silhouette scores for the valid clusters
    #     valid_silhouette_scores = [silhouette_scores[i] for i in valid_indices]
    #     # valid clusters
    #     valid_keys = [keys[i] for i in valid_indices]
        
    #     valid_thresholds = [self.dict_of_scores[key]["threshold"] for key in valid_keys]
    #     valid_clusters = [self.dict_of_scores[key]["clusters"] for key in valid_keys]
        
    #     p_value_json = {}
    #     for i, cluster in enumerate(valid_clusters):
    #         p_value_matrix = self.simulate_pwes(valid_thresholds[i], 10000, "silhouette")
    #         p_value_json[len(p_value_matrix)] = p_value_matrix.tolist()


    #     # simulate with threshold 10
    #     p_value_matrix = self.simulate_pwes(10, 10000, "threshold_10")
    #     p_value_json[len(p_value_matrix)] = p_value_matrix.tolist()
        
    #     with open(f"figures/{self.protein_name}/{self.suffix}/{self.pdb_name}/p_values.json", "w") as f:
    #         json.dump(p_value_json, f)
        
    #     return None


    # def simulate_pwes(self, threshold, n_simulations, based_on):
    #     clusters = sch.fcluster(self.linkage_matrix, t=threshold, criterion='distance')
    #     result_array = self.PWES_array
    #     xij_array = self.xij_array
    #     dij_array = self.dij_array
    #     gene = self.protein_name
    #     experiment = self.suffix
    #     t = 16
    #     unique_clusters = np.unique(clusters)
    #     xij_mean = np.mean(xij_array)
    #     xij_std = np.std(xij_array)
    #     residue_range = np.arange(0, dij_array.shape[0])

    #     def pwes(xij, dij, xij_mean, xij_std, t):
    #         return np.tanh((xij - xij_mean) / xij_std) * np.exp(-((dij**2) / (2*(t**2))))

    #     sim_types = ["residues", "scores"]
    #     p_value_matrix = np.zeros((len(unique_clusters), len(sim_types)))

    #     plt.figure(figsize=(10, 20))
    #     # big figure title
    #     plt.suptitle(f"Gene: {gene}, Experiment: {experiment}, Number of Clusters: {len(unique_clusters)}, Threshold: {threshold}, Based on: {based_on}", fontsize=16)
    #     for sim_type_idx, sim_type in enumerate(sim_types):
    #         for cluster_idx, cluster in enumerate(unique_clusters):
    #             cluster_indices = np.where(clusters == cluster)[0]
    #             cluster_result_array = result_array[cluster_indices, :][:, cluster_indices]
    #             sim_sum_array = np.zeros(n_simulations)

    #             all_rand_res = np.random.choice(residue_range, (n_simulations, 2, cluster_result_array.shape[0]), replace=True)
    #             cluster_xij_array = xij_array[cluster_indices, :][:, cluster_indices]
    #             cluster_dij_array = dij_array[cluster_indices, :][:, cluster_indices]
    #             for sim in range(n_simulations):
    #                 sim_indices = np.ix_(all_rand_res[sim, 0], all_rand_res[sim, 0])
    #                 if sim_type == "residues":
                        
    #                     simulated_pwes = pwes(cluster_xij_array, dij_array[sim_indices], xij_mean, xij_std, t)
                                            

    #                 elif sim_type == "scores":
    #                     simulated_pwes = pwes(xij_array[sim_indices], cluster_dij_array, xij_mean, xij_std, t)

    #                 np.fill_diagonal(simulated_pwes, 0)  # To exclude diagonal elements
    #                 sim_sum_array[sim] = np.sum(np.abs(simulated_pwes))

    #             obs_sum = np.sum(np.abs(pwes(xij_array[cluster_indices, :][:, cluster_indices],
    #                                     dij_array[cluster_indices, :][:, cluster_indices], 
    #                                     xij_mean, xij_std, t)))

                
    #             # calculate empirical p-value
    #             if sim_type == "residues":
    #                 p_value = (np.sum(sim_sum_array >= obs_sum) +1)/ (n_simulations+1)
                    
    #             if sim_type == "scores":
    #                 p_value = np.min([(np.sum(sim_sum_array >= obs_sum) +1)/ (n_simulations+1), (np.sum(sim_sum_array <= obs_sum) +1) / (n_simulations +1)])

    #             p_value_matrix[cluster_idx, sim_type_idx] = p_value

    #             # Plot histogram
    #             plt.subplot(len(unique_clusters), len(sim_types), cluster_idx * len(sim_types) + sim_type_idx + 1)
    #             plt.hist(sim_sum_array, bins=50)
    #             plt.axvline(obs_sum, color='r')
    #             plt.title(f"Cluster {cluster}, {sim_type}, p-value: {p_value:.1e}, Observed sum: {obs_sum:.2f}", fontsize=9)
            
    #     plt.subplots_adjust(wspace=0.4, hspace=2)  # Adjust the space between subplots
    #     plt.savefig(f"figures/{gene}/{experiment}/{self.pdb_name}/{gene}_simulated_pwes_{len(unique_clusters)}_clusters_{threshold}_{based_on}.pdf")
        
    #     plt.close()

    #     return p_value_matrix
