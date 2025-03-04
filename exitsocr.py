import cv2, os
import numpy as np
from sklearn.cluster import DBSCAN
sift = cv2.SIFT_create()
large_image = cv2.imread(f'stations_png\\Tsim Sha Tsui.png', cv2.IMREAD_COLOR)
kp2, des2 = sift.detectAndCompute(large_image, None)
# Load images
for exit in os.listdir(os.getcwd()+"\\oldexits"):
    exit_sub_image = cv2.imread(os.getcwd()+"\\oldexits\\"+exit, cv2.IMREAD_COLOR)

    # Initialize SIFT detector
    

    # Find keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(exit_sub_image, None)

    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # Apply ratio test
    good = []
    for m, n in matches:
        if m.distance < 0.9 * n.distance:
            good.append(m)
    # Extract coordinates of good matches in the large image
    coordinates = np.array([kp2[match.trainIdx].pt for match in good])
    
    if len(coordinates) == 0:
        continue
    # Apply DBSCAN clustering
    clustering = DBSCAN(eps=50, min_samples=2).fit(coordinates)
    labels = clustering.labels_

    # Extract unique clusters and their match counts
    unique_labels = set(labels)
    clusters = {label: coordinates[labels == label] for label in unique_labels if label != -1}

    # Calculate and print matching percentages for each cluster
    for label, cluster_coords in clusters.items(): 
        matching_percentage = (len(cluster_coords) / len(kp1)) * 100
        print(f"Cluster {label}: Matching percentage for exit {exit[:-4]}: {matching_percentage:.2f}%")
        print(f"Coordinates of matched keypoints for cluster {label+1}:")
        for (x, y) in cluster_coords:
            print(f"({x:.2f}, {y:.2f})")

    # Draw matches and clusters
    img_matches = cv2.drawMatches(exit_sub_image, kp1, large_image, kp2, good, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    for label, cluster_coords in clusters.items():
        for (x, y) in cluster_coords:
            cv2.circle(img_matches, (int(x), int(y + exit_sub_image.shape[0])), 10, (0, 255, 0), 2)

    if "c2" in exit:
        print(coordinates)
        cv2.imshow(f'Matches for {exit}', img_matches)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    