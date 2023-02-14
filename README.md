# DocumentBot
RASA chatbot for Q&A from document


## Installation

### Local

1. Clone the DocumentBot project.

```
https://github.com/duttarnab/DocumentBot.git
```

2. Install python3, pip (https://rasa.com/docs/rasa/installation/environment-set-up).

3. Install Rasa

```
pip3 install rasa
```

4. Go to project directory `DocumentBot` and train the project model

```
cd <path_to_project_folder>
rasa train
```

5. Starts a server with your trained model.

```
rasa run -m models --endpoints endpoints.yml --enable-api --cors "*"
```

6. On another terminal start rasa actions.

```
cd <path_to_project_folder>
rasa run actions
```

7. Once it is started open <path_to_project_folder>/index.html on browser to test the chatbot.
