<?php
require 'vendor/autoload.php';

use Google\Cloud\Firestore\FirestoreClient;

function getEmailsFromFirestore() {
    // Initialize Firestore Client
    $firestore = new FirestoreClient([
        'projectId' => 'kingaboravaccinationsystem' 
    ]);

    // Reference to the 'parentData' collection
    $parentDataCollection = $firestore->collection('parentData');

    // Fetch documents and extract emails
    $emails = [];
    $documents = $parentDataCollection->documents();

    foreach ($documents as $document) {
        if ($document->exists()) {
            $email = $document->data()['parentEmailAddress'];
            if (!empty($email)) {
                $emails[] = $email;
            }
        }
    }

    return $emails;
}

// Usage
$emailArray = getEmailsFromFirestore();
print_r($emailArray);


?>