import csv

def compare_predictions(svm_file, nb_file, output_file):
    svm_predictions = {}
    nb_predictions = {}
    
    # Read SVM predictions
    with open(svm_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            svm_predictions[row['instance_id']] = row['genre']
    
    # Read NB predictions
    with open(nb_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            nb_predictions[row['instance_id']] = row['genre']
    
    # Compare and write results
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['instance_id', 'genre'])
        writer.writeheader()
        
        for instance_id in svm_predictions.keys():
            svm_pred = svm_predictions[instance_id]
            nb_pred = nb_predictions[instance_id]
            
            if svm_pred in ['comedy', 'Opera']:
                final_pred = svm_pred
            else:
                final_pred = nb_pred
            
            writer.writerow({'instance_id': instance_id, 'genre': final_pred})

# Usage
svm_file = '../data/outputs/test_predictionsNB.csv'
nb_file = '../data/outputs/test_predictions2.csv'
output_file = '../data/outputs/output_predictionsVote2.csv'

compare_predictions(svm_file, nb_file, output_file)