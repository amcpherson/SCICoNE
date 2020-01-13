import os
import subprocess
from snakemake.workflow import Workflow, Rules
import snakemake.workflow
from snakemake import shell
from snakemake.logging import setup_logger
import numpy as np
import pandas as pd
import graphviz

# See https://gist.github.com/marcelm/7e432275dfa5e762b4f8 on how to run a
# Snakemake workflow from Python

class Tree(object):
    def __init__(self):
        self.traces = None
        self.best_scores = None
        self.graphviz_str = None

    def read_from_file(self, file):
        self.graphviz_str = f"hello, this is the graphviz string for the tree in {file}"

    def learn_tree(self, data):
        pass

    def plot_tree(self, show_genes=True):
        pass


class SCICoNE(object):
    """
    This class  provides an interface to interact with the outputs from the C++
    program that infers a copy number phylogeny from single-cell WGS data.

    It exposes functions to visualize breakpoint detection results, annotate
    the bins, and plot the resulting trees. Its attributes can be further
    processed using scgenpy, a generic package for pre, post-processing and
    visualization of single-cell copy number data.
    """
    def __init__(self, binary_path, output_path, persistence=False):
        """Create a SCICoNE object.

        binary_path : type
            Path to SCICoNE binaries.
        output_path : type
            Path to SCICoNE output files.
        persistence : boolean
            Wether to delete output files from C++ after loading them into the class.
        """
        self.binary_path = binary_path
        self.simulation_binary = os.path.join(self.binary_path, 'simulation')
        self.bp_binary = os.path.join(self.binary_path, 'breakpoint_detection')
        self.inference_binary = os.path.join(self.binary_path, 'inference')
        self.score_binary = os.path.join(self.binary_path, 'score')

        self.output_path = output_path
        self.persistence = persistence
        self.postfix = 'PYSCICONETEMP'

        self.n_cells = 0
        self.n_nodes = 0
        self.best_tree = None
        self.tree_list = []

    def simulate_data(self, n_cells=200, n_nodes=5, n_bins=1000, n_regions=40, n_reads=10000, nu=1.0, ploidy=2, verbosity=0):
        cwd = os.getcwd()
        output_path = os.path.join(self.output_path, f"simulation_{self.postfix}")
        try:
            os.mkdir(output_path)
            os.chdir(output_path)
        except OSError as e:
            print("OSError: ", e.returncode, e.output, e.stdout, e.stderr)

        try:
            cmd_output = subprocess.run([self.simulation_binary, f"--n_cells={n_cells}", f"--n_nodes={n_nodes}",\
                f"--n_regions={n_regions}", f"--n_bins={n_bins}", f"--n_reads={n_reads}", f"--nu={nu}",\
                f"--ploidy={ploidy}", f"--verbosity={verbosity}", f"--postfix={self.postfix}"])
        except subprocess.SubprocessError as e:
            print("SubprocessError: ", e.returncode, e.output, e.stdout, e.stderr)

        # The binary generates 4 files: *_d_mat.csv, *_ground_truth.csv, *_region_sizes.txt and *_tree.txt.
        # We read each one of these files into np.array, np.array, np.array and Tree structures, respectively,
        # and output a dictionary with keys "d_mat", "ground_truth", "region_sizes" and "tree".
        d_mat_file = os.path.join(output_path, f"{n_nodes}nodes_{n_regions}regions_{n_reads}reads_{self.postfix}_d_mat.csv")
        ground_truth_file = os.path.join(output_path, f"{n_nodes}nodes_{n_regions}regions_{n_reads}reads_{self.postfix}_ground_truth.csv")
        region_sizes_file = os.path.join(output_path, f"{n_nodes}nodes_{n_regions}regions_{n_reads}reads_{self.postfix}_region_sizes.txt")
        tree_file = os.path.join(output_path, f"{n_nodes}nodes_{n_regions}regions_{n_reads}reads_{self.postfix}_tree.txt")

        output = dict()
        output['d_mat'] = np.loadtxt(d_mat_file, delimiter=',')
        output['ground_truth'] = np.loadtxt(ground_truth_file, delimiter=',')
        output['region_sizes'] = np.loadtxt(region_sizes_file, delimiter=',')

        tree = Tree()
        tree.read_from_file(tree_file)

        output['tree'] = tree

        # Now that we've read all outputs into memory, we delete the temporary files if persistence==False
        if not self.persistence:
            os.remove(d_mat_file)
            os.remove(ground_truth_file)
            os.remove(region_sizes_file)
            os.remove(tree_file)
            os.rmdir(output_path)

        os.chdir(cwd)
        return output


    def detect_breakpoints(self):
        pass

    def learn_tree(self, n_reps=10):
        # run tree bin using the complete snakemake workflow

        # if multiple reps:
        # read in all traces
        # pick best tree

        # load best tree

        if not self.persistence:
            # delete files
            pass

    def plot_bps(self, cluster_cells=True):
        pass
