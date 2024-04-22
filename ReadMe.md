Before executing the apis, create a virtual environment using the command:
        
        python3 -m <v_env_name> venv
Then activate the environment by:

         source venv/bin/activate

After activating the virtual environment, need to install the pre-requisites
For that install the requirement.txt file by:

            pip3 install -r requirements.txt

Now to execute all the apis:
            
            uvicorn main:app --reload

uvicorn will be running:
    
            http://127.0.0.1:8000

Also the below url will have all the interactive API docs

            http://127.0.0.1:8000/docs

Also created a Architecture_Explanation.txt file where the architecture has
been explained.