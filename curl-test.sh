#!/bin/bash



# GET METHOD TEST
( curl -sX GET http://localhost:5000/api/timeline_post > .tmp_file)
if [[ $? ]]
then
    echo "GET test passed"
else 
    echo "GET test failed"
    exit 1
fi


# POST METHOD TEST
id=$( curl -sX POST http://localhost:5000/api/timeline_post -d "name=Wei&email=wei.he@mlh.io&content=Testing my endpoints with postman and curl." | grep -E -0 "id\":[0-9]+" | cut -d":" -f2 )
if [[ $? ]]
then
    echo "POST test passed"
else
    echo "POST test failed"
    exit 1
fi


# DELETE METHOD TEST
(curl -sX DELETE http://localhost:5000/api/timeline_post -d "id=$id" > .tmp_file)
if [[ $? ]]
then
    echo "DELETE test passed"
else 
    echo "DELETE test failed"
    exit 1
fi


echo "All method tests passed"
rm -f .tmp_file


