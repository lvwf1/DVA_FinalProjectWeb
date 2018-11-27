# DVA_FinalProjectWeb

### Prerequisite: Python 3.6, Pycharm IDE, RStudio, Spyder

### Required Packages for Python 3.6: flask, flask_restful, flask_cors, pandas, numpy, matplotlib, sklearn, keras, tensorflow, collections

## a. Player Evaluation
FinalProject_BackEnd:
Run with PyCharm:
1. Import files into PyCharm Project with Flask Template with Default Settings, install All required packeages to virtual environment
2. Run DVA_FinalProjectWeb in PyCharm directly OR Use PyCharm Terminal then enter command: python.exe -m flask run
3. The application is running localhost under http://localhost:5000/ by default
Run with Terminal:
1. Open Terminal, pip all required packeages in terminal
2. cd <path>/FinalProject_BackEnd, python.exe -m flask run
3. The application is running localhost under http://localhost:5000/ by default

FinalProject_FrontEnd:
1. cd <path>/FinalProject_FrontEnd
2. python -m http.server
3. The application is running localhost under http://localhost:8000/ by default
4. Run http://localhost:8000/player.html to see the player analysis visualization
  
## b. Team Evaluation
FinalProject_BackEnd
1. Run Team_Evaluation.Rmd in RStudio to get the evaluation result as well as visualiztion

FinalProject_FrontEnd
1. Run http://localhost:8000/team.html to see the team analysis visualization 

## c. Champion Evaluation
FinalProject_BackEnd
1. Run main_champion.py in Spyder to get the prediction and validation result

FinalProject_FrontEnd
1. Run http://localhost:8000/ChampionPrediction.html or http://localhost:8000/champion.html to see the champion prediction visualization 
