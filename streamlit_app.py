import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
from fisher_model_simulation import FisherModelSimulation
import json
import numpy as np
from sklearn.decomposition import PCA


# Załadój parametry z pliku JSON
params = None
historia_populacji = None

# Lista do kroków, w których będzie katastrofa
red_flash_frames = []

# Initialize Streamlit app
st.title('Fisher Model Simulation')

# Sidebar for JSON file upload
st.sidebar.title("Upload JSON File")
uploaded_file = st.sidebar.file_uploader("Choose a JSON file", type="json")

# main part
st.text('Symulacja ewolucji populacji w zmieniającym się środowisku')
# st.text('Założenia:')
st.text('Reprodukcja płciowa, nielosowy wybór partnera')
st.text('Każdy może spotkać się z każdym, osobniki tworzą jedną parę na krok czasowy')
st.text('Preferencja osobników żeńskich -> druga współrzędna osobników męskich < 0.8 \nJeśli takiego osobnika brak, bierze z najmniejszą drugą współrzędną')
# W efekcie dojdzie do kompromisu pomiędzy dostosowaniem a non-random mating


# Display parameters from uploaded JSON file
if uploaded_file is not None:
    params = json.load(uploaded_file)
    st.sidebar.subheader('Simulation Parameters')
    for key, value in params.items():
        st.sidebar.text(f"{key}: {value}")

# Display simulation start button
if params is not None:
    if st.button("Start Simulation"):
        # Load simulation
        simulation = FisherModelSimulation(params)
        historia_populacji, red_flash_frames, optima = simulation.run_simulation()

        all_genotype_features = []

        for step in historia_populacji:
            for individual in step:
                genotype_features = individual[0]  
                all_genotype_features.append(genotype_features)
        genotype_array = np.array(all_genotype_features)
        pca = PCA(n_components=2)
        reduced_data = pca.fit_transform(genotype_array)
        transformation_matrix = pca.components_

        optima = np.array(optima)

        optima_points_transformed = np.dot(optima, transformation_matrix.T)

        reduced_data_index = 0

        for step in historia_populacji:
            for individual in step:
                # Replace the genotype features with the corresponding reduced data
                individual[0] = reduced_data[reduced_data_index]
                reduced_data_index += 1


# Display scatter plot animation and population size over time
if historia_populacji is not None:
    st.subheader('Genomy osobników w czasie')
    st.text('PCA dla wielu genów')
    fig, ax = plt.subplots()
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    scat = ax.scatter([], [])

    def init():
        scat.set_offsets(np.empty((0, 2)))
        return scat,

    def update(frame):
        ax.clear()
        ax.set_xlim(min(reduced_data[:, 0].min(), optima_points_transformed[:, 0].min())-0.2, max(reduced_data[:, 0].max(), optima_points_transformed[:, 0].max())+0.2)
        ax.set_ylim(min(reduced_data[:, 1].min(), optima_points_transformed[:, 1].min())-0.2, max(reduced_data[:, 1].max(), optima_points_transformed[:, 1].max())+0.2)
        if frame < len(historia_populacji):
            x_data = [ind[0][0] for ind in historia_populacji[frame]]
            y_data = [ind[0][1] for ind in historia_populacji[frame]]
            sex_data = [ind[1] for ind in historia_populacji[frame]]
            if frame in red_flash_frames:
                ax.scatter(x_data, y_data, color='red', s=5)
            else:
                female_indices = [i for i, sex in enumerate(sex_data) if sex == 0]
                male_indices = [i for i, sex in enumerate(sex_data) if sex == 1]
                ax.scatter(np.array(x_data)[male_indices], np.array(y_data)[male_indices], color='lightgreen', s=5, label='Male')
                ax.scatter(np.array(x_data)[female_indices], np.array(y_data)[female_indices], color='darkblue', s=5, label='Female')
                ax.scatter([optima_points_transformed[frame, 0]], [optima_points_transformed[frame, 1]], color='orange', marker='x', label='Optimum')
                ax.legend()
        return scat,


    ani = FuncAnimation(fig, update, frames=range(len(historia_populacji)), init_func=init, blit=True)
    plt.legend(['Male', 'Female'], loc='upper left')
    ani.save('animation.gif', writer=PillowWriter(fps=4))
    st.image('animation.gif')

    st.subheader('Population Size Over Time')
    population_sizes = [len(step) for step in historia_populacji]
    plt.figure()  # Create a new figure for the population size plot
    plt.plot(range(params['num_steps']), population_sizes, marker='o', linestyle='-', color='orange', markersize=3)
    plt.title('Population Size Over Time')
    plt.xlabel('Time Step')
    plt.ylabel('Population Size')
    plt.grid(True)
    st.pyplot(plt)

# konserwacja drugiej cechy na wykresie