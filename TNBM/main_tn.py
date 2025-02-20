#
# DA FARE: 
# Ricorda! E' un modello implicito, quindi non conosciamo la distribuzione target (nell'esempio toy facciamo finta di non conoscerla)
# Bisogna aggiustare la MMD. Al momento è come quella di di Oriel con exact True, ci serve l'altra, cioè quella per i sample.
# Il training non si può fare con autograd così com'è. Bisogna fare un training loop e fare i gradienti con parameter shift.
# Bisogna capire come si fa a rendere la bond dimension una roba addestrabile
# 
import sys
import json
import numpy as np
import math
import quimb as qu
import jax
import jax.numpy as jnp
import quimb as qu
import quimb.tensor as qtn

from functions import *


PATH = "parameters.json"
SAMPLE_BITSTRING_DIMENSION, PRINT_TARGET_PDF, DEVICE, EPOCHS = load_parameters(PATH)
jax.config.update("jax_platform_name", DEVICE)
np.random.seed(42)
n_qubits = SAMPLE_BITSTRING_DIMENSION


def main():
    ######################################################################################################################################################
    # Building dataset. We will then provide the model one data at the time and calculate MMD for each sample
    #
    dataset = get_bars_and_stripes(int(math.sqrt(SAMPLE_BITSTRING_DIMENSION)))
    if PRINT_TARGET_PDF == True:
        print_bitstring_distribution(dataset)

    ######################################################################################################################################################
    # MPS initialization. The number of open indexes controls the number of nodes in the MPS, and thus the number of 
    # gate blocks. Bond_dimension represent maximum bond dimension, that controls the expressivity of the model.
    # bond_dimension = 2^(D/2) where N is the number of qubits of the largest state exactly representable.
    # TO DO: bond dimension should be some kind of variable
    #
    number_open_index = 9
    bond_dimension =   2**8
    psi = qtn.MPS_rand_state(L=number_open_index, bond_dim=bond_dimension)
    print("MODEL:")
    print(psi)
    print()
    tensor_array = []
    for site, tensor in psi.tensor_map.items():
        tensor_array.append(tensor.data)

    sys.exit()
    
    ######################################################################################################################################################
    # Initialize MMD
    #

    bandwidth = np.array([0.25, 0.5, 1])
    space = np.arange(2**n_qubits)
    mmd = MMD(bandwidth, space)


    ######################################################################################################################################################
    # OPTIMIZATION
    # We have to understand which are our parameters. We have to give a fitting format to data to be given to tn.
    # At every loop of r we change learning rate for convergence.
    # At every epoch we wanto to compute gradients to update the MPS. We calculate the MMD loss inside the gradient computation.
    #

    # PARAMETERS INITIALIZATION
    #-----------------------------------------------------------------------------------------------------------------------------------------------------
    rep = 10
    lr0 = 0.1
    np.random.seed(seed)
    parameters = np.random.normal(0, np.pi, size  = n_param)
    parameters[1:] = 0
    optimizer = ADAM(n_param, lr = lr0)
    seed = 12+42 + 53*(1+r)

    for ep in range(EPOCHS):

        # LOADING SAMPLE
        #-----------------------------------------------------------------------------------------------------------------------------------------------------
        optimizer._lr = lr
        np.random.shuffle(target)
        target_train = target[:batch_size,...]
        median_grad = []
        global intermediary_tv
        intermediary_tv = []


        # COMPUTING LOSS FUNCTION FOR LOG
        #-----------------------------------------------------------------------------------------------------------------------------------------------------
        "......................."


        # COMPUTING GRADIENTS
        #-----------------------------------------------------------------------------------------------------------------------------------------------------
        for _ in range(grad_batch):

            gradients = compute_gradient(ansatz, parameters, target_train, qubits, n_shots,grad_loss_function, signal = signal, exact = exact, values = values)
            median_grad.append(gradients)

        temp_grad = np.mean(np.mean(np.array(median_grad), axis=0), axis=-1).reshape(-1)


        # PARAMETERS UPDATE
        #-----------------------------------------------------------------------------------------------------------------------------------------------------
        parameters = optimizer.update(parameters,temp_grad)


        # CHECKING CONVERGENCE AND PRINTING
        #-----------------------------------------------------------------------------------------------------------------------------------------------------
        if np.linalg.norm(new_params - params) < tol:
            print(f'Converged in {iteration + 1} iterations.')
            return new_params    

        params = new_params
        
        if (iteration + 1) % 100 == 0:
            print(f'Iteration {iteration + 1}: cost = {cost:.6f}, ||grad|| = {np.linalg.norm(grad):.6f}')

    print("Maximum iterations reached.")
    return params


if __name__ == "__main__":
    main()