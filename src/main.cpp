#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <map>
#include <string>

#include <iterator>


#include "MathOp.h"
#include "Tree.h"
#include "Inference.h"
#include "../tests/validation.h"


using namespace std;

vector<vector<double>> read_counts(const string path)
{
    /*
     * Parses the input data into a double vector.
     * */
    vector<vector<double>> mat;

    std::ifstream filein(path);

    int i = 0, j=0;
    for (std::string line; std::getline(filein, line); )
    {

        // push an empty vector
        mat.push_back(vector<double>());

        std::istringstream fline(line);
        j = 0;
        for(;;) {
            double val;
            fline >> val;
            if (!fline) break;
            mat[i].push_back(val);
            j++;
        }
        i++;

    }
    return mat;
}

void disp_vec(vector<vector<double>> vec) {
/*
 * displays the double vector
 * */

    for (auto const &v1: vec) {
        for (auto const &v2: v1)
            cout << v2 << ' ';
        cout << endl;
    }
}


int main() {

    test_xxhash();
    test_swap_label();
    test_weighted_sample();
    test_prune_reattach();
    test_weighted_prune_reattach();
    test_add_remove_event();

    // counts per region per cell
    vector<vector<int>> D = {{39,37,45,49,30},{31,28,34,46,11},{69,58,68,34,21},{72,30,31,46,21},{50,32,20,35,13}};

    // region sizes
    vector<int> r = {4,2,3,5,2};

    // move probabilities
    vector<float> move_probs = {1.0f,1.0f,1.0f,1.0f, 1.0f};

    Inference mcmc(size(r));

    // mcmc.initialize_worked_example();
    mcmc.random_initialize();
    mcmc.compute_t_table(D,r);
    disp_vec(mcmc.t_scores);

    mcmc.infer_mcmc(D, r, move_probs);
    mcmc.write_best_tree();

    mcmc.destroy();



    // parse input
    vector<vector<double>> mat;
    mat = read_counts("/Users/mtuncel/git_repos/sc-dna/input_data/norm_counts.tsv");

    // compute the AIC scores
    u_int window_size = 3;
    vector<vector<double>> aic_vec = MathOp::likelihood_ratio(mat,window_size);


    // dynamic programming
//    for (auto const &v2: aic_vec[11])
//        cout << v2 << ' ';
//    cout << endl;

    //auto n_aic_vec = log_normalize(aic_vec[0]);
    vector<vector<double>> sigma;
    vector<double> priors;
    int n_breakpoints = aic_vec.size();
    int n_cells = aic_vec[0].size();
    cout <<"n_breakpoints: " << n_breakpoints << " n_cells: " << n_cells <<endl;
    int i = 0;
    for (auto vec: aic_vec) // compute sigma matrix
    {
        cout << i++ <<" --> ";
        auto res = MathOp::combine_scores(vec);
        sigma.push_back(res);
        for (auto const &v2: res)
            cout << v2 << ' ';
        cout <<endl;

    }

    for (int j = 0; j < n_cells; ++j) {
        priors.push_back(MathOp::breakpoint_log_prior(j, n_cells,0.5));
    }

    vector<vector<double>> posterior;
    //double posterior[n_breakpoints][n_cells];

    for (int k = 0; k < n_breakpoints; ++k) {
        posterior.push_back(vector<double>());
        for (int j = 0; j < n_cells; ++j) {
            double val = priors[j] + sigma[k][j];
            posterior[k].push_back(val);
            //cout << posterior[k][j];
        }
    }
    int k_star = 2;

    vector<double> s_p;

    for (int l = 0; l < n_breakpoints; ++l)
    {
        double sum_from_k_star = std::accumulate(posterior[l].begin()+k_star, posterior[l].end(), 0.0);
        double sum_till_kstar = std::accumulate(posterior[l].begin(), posterior[l].begin()+k_star, 0.0);
        s_p.push_back(sum_from_k_star / (sum_from_k_star + sum_till_kstar));
    }

    std::ofstream output_file("./s_p.txt");
    for (const auto &e : s_p) output_file << e << "\n";
    return 0;
}
