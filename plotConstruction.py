#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 13:57:06 2024

@author: jtvendetti
"""

import numpy as np
import matplotlib.pyplot as plt




# Define the PCA function
def pca(X, out_dim):
    X = np.copy(X)
    D = X.shape[0]  # feature dimension
    N = X.shape[1]  # number of data instances

    # Step 1: Compute the mean vector mu
    mu = np.mean(X, axis=1, keepdims=True)

    # Step 2: Subtract the mean vector from the data to center the data

    X_centered = X - mu


    # Step 3: Compute the covariance matrix Sigma
    Sigma = np.matmul(X_centered, X_centered.T) / N

    # Step 4: Perform eigendecomposition on the covariance matrix
    eigvals, eigvecs = np.linalg.eigh(Sigma)
    
    # Step 5: Sort the eigenvalues and eigenvectors in descending order
    sorted_indices = np.argsort(eigvals)[::-1]
    eigvals = eigvals[sorted_indices]
    eigvecs = eigvecs[:, sorted_indices]

    # Step 6: Select the top 'out_dim' eigenvectors
    W = eigvecs[:, :out_dim]

    return mu, W

# Reconstruct the image using the PCA projection matrix
def reconstruct(X, mu, W):

    X_projected = np.matmul(W.T, (X - mu))
    

    # Reconstruct from lower-dimensional space
    X_reconstructed = np.matmul(W, X_projected) + mu
    return X_reconstructed

# Define the function to compute reconstruction error
def reconstruction_error(X_test, mu, W):
    X_projected = np.matmul(W.T, (X_test - mu))

    # Reconstruct from lower-dimensional space
    X_reconstructed = np.matmul(W, X_projected) + mu
    error = np.mean((X_test - X_reconstructed) ** 2)
    return error

def main():
    # Flatten the images and normalize the data
    data = np.loadtxt('mnist_test.csv', delimiter=',')

# Split the dataset into images (X) and labels (y)
    X = data[:, :-1]  # All columns except the last one are the pixel values
    y = data[:, 0]

    print("Shape of X (images):", X.shape)
    print("Shape of y:", y.shape)
# Select only images of digit 3
    X_digit3 = X[y == 3]
    print("Shape of X_digit3:", X_digit3.shape)

    if X_digit3.shape[0] > 0:  # Ensure there are images of digit 3
        sample_image = X_digit3[0, :] # Select the first image
        print("Shape of sample_image:", sample_image.size)
        if sample_image.size == 784:
            sample_image = sample_image.reshape(28, 28)
            print("Sample image reshaped to (28, 28)")
            dimensions = [2, 8, 64, 128, 784]

            # Perform PCA and reconstruct the image for each dimension
            reconstructions = []
            for dim in dimensions:
                mu, W = pca(X_digit3, out_dim=dim)
                reconstruction = reconstruct(X_digit3, mu, W)
                reconstructions.append(reconstruction)

            # Plot original image and its PCA reconstructions
            plt.figure(figsize=(10, 5))

            # Plot original image
            plt.subplot(1, 6, 1)
            plt.imshow(sample_image, cmap='gray')
            plt.title('Original')

            # Plot PCA reconstructed images
            for i, reconstruction in enumerate(reconstructions):
                plt.subplot(1, 6, i + 2)
                plt.imshow(sample_image, cmap='gray')
                plt.title(f'{dimensions[i]} PCs')

            plt.tight_layout()
            plt.show()
        else:
            print(f"Error: Sample image does not have 784 elements, instead it has {sample_image.size} elements")
    else:
        print("Error: No digit 3 images found in the dataset.")



# Define a set of 100 images of digit 3 as a test set
    X_test = X_digit3[:, :100]

# Select images for case b (digits 3 and 8) and case c (digits 3, 8, and 9)
    X_digit38 = X[(y == 3) | (y == 8)]
    print("Shape of X_digit38:", X_digit38.shape)
    if X_digit38.shape[0] > 0:
        X_digit38 = X_digit38.reshape(-1, X_digit38.shape[1])
    else:
        print("Error: No digit 3 or 8 images found in the dataset.")

    X_digit389 = X[(y == 3) | (y == 8) | (y == 9)]
    print("Shape of X_digit389:", X_digit389.shape)
    if X_digit389.shape[0] > 0:
        X_digit389 = X_digit389.reshape(-1, X_digit389.shape[1])
    else:
        print("Error: No digit 3 or 8 or 9images found in the dataset.")

# Range of PCA dimensions
    dims_range = np.arange(10, 784, 10)


    errors_case_a = []
    errors_case_b = []
    errors_case_c = []

    for dim in dims_range:
        mu_a, W_a = pca(X_digit3, out_dim=dim)
        mu_b, W_b = pca(X_digit38, out_dim=dim)
        mu_c, W_c = pca(X_digit389, out_dim=dim)

        error_a = reconstruction_error(X_digit3, mu_a, W_a)
        error_b = reconstruction_error(X_digit38, mu_b, W_b)
        error_c = reconstruction_error(X_digit389, mu_c, W_c)

        errors_case_a.append(error_a)
        errors_case_b.append(error_b)
        errors_case_c.append(error_c)

# Plot reconstruction errors for all three cases
    plt.figure(figsize=(10, 6))
    plt.plot(dims_range, errors_case_a, label='Digit 3', color='blue')
    plt.plot(dims_range, errors_case_b, label='Digit 3 and 8', color='orange')
    plt.plot(dims_range, errors_case_c, label='Digit 3, 8, and 9', color='green')
    plt.xlabel('Number of Principal Components')
    plt.ylabel('Reconstruction Error')
    plt.title('Reconstruction Error vs Number of Principal Components')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
