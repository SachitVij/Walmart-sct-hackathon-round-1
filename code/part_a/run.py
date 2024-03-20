import pandas as pd
from geopy.distance import geodesic
import os

def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).kilometers

def find_next_closest_node(current_node, nodes, visited):
    min_distance = float('inf')
    next_node = None
    for node in nodes:
        if node not in visited:
            distance = calculate_distance(current_node, node)
            if distance < min_distance:
                min_distance = distance
                next_node = node
    return next_node, min_distance

def process_dataset(input_file, output_file):
    df = pd.read_csv(input_file)
    depot_coord = (df.iloc[0]['depot_lat'], df.iloc[0]['depot_lng'])
    order_coords = [(row['lat'], row['lng']) for index, row in df.iterrows()]
    visited = {depot_coord: 0}
    current_node = depot_coord
    total_distance = 0
    
    while len(visited) < len(order_coords) + 1:
        next_node, distance = find_next_closest_node(current_node, order_coords, visited)
        total_distance += distance
        visited[next_node] = len(visited)
        current_node = next_node
    
    df['dlvr_seq_num'] = df.apply(lambda row: visited[(row['lat'], row['lng'])], axis=1)
    df_output = df[['order_id', 'lng', 'lat', 'depot_lat', 'depot_lng', 'dlvr_seq_num']]
    df_output.to_csv(output_file, index=False)
    
    return total_distance

def main(input_dir='input_datasets', output_dir='output_datasets'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    distances = []
    for file_name in sorted(os.listdir(input_dir)):
        if file_name.startswith("part_a_input_dataset_") and file_name.endswith(".csv"):
            input_file_path = os.path.join(input_dir, file_name)
            output_file_name = file_name.replace('input', 'output')
            output_file_path = os.path.join(output_dir, output_file_name)
            distance = process_dataset(input_file_path, output_file_path)
            distances.append((file_name, distance))
            print(f"Processed {input_file_path} -> {output_file_path}, Distance: {distance} kms")

    summary_df = pd.DataFrame(distances, columns=['Dataset', 'Best Route Distance'])
    summary_df['Best Route Distance'] = summary_df['Best Route Distance'].apply(lambda x: f"{x} kms")
    summary_df.to_csv('part_a_best_routes_distance_travelled.csv', index=False)

if __name__ == "__main__":
    main()