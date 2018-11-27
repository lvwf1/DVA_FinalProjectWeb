# DVA_FinalProjectWeb

### DESCRIPTION
The project is completed by CSE6242 Data Visual Analytics Team80, NBA Players and Teams Analysis
Team Members: Zibin Chen, Weifeng Lyu, Zeyu Ni, Jingya Qin, Jian Zhan, Yang Zhang

### INSTALLATION
## Prerequisite: Python 3.6, Pycharm IDE, RStudio, Spyder
## Required Packages for Python 3.6: flask, flask_restful, flask_cors, pandas, numpy, matplotlib, sklearn, keras, tensorflow, collections

Clone this repository, Import <path>/FinalProject_BackEnd project files into PyCharm Project with Flask Template with Default Settings, install All required packeages to python virtual environment

### EXECUTION
## a. Player Evaluation
FinalProject_BackEnd:
1. Clone this repository, Import <path>/FinalProject_BackEnd project files into PyCharm Project with Flask Template with Default Settings, install All required packeages to python virtual environment
2. Run DVA_FinalProjectWeb in PyCharm directly OR Use PyCharm Terminal then enter command: python.exe -m flask run
3. The back-end application is running localhost under http://localhost:5000/ by default
  OR
1. Open Terminal, pip all required packeages in terminal
2. cd <path>/FinalProject_BackEnd, python.exe -m flask run
3. The back-end application is running localhost under http://localhost:5000/ by default

FinalProject_FrontEnd:
1. Open Terminal, cd <path>/FinalProject_FrontEnd
2. python -m http.server
3. The front-end application is running localhost under http://localhost:8000/ by default
4. Run http://localhost:8000/player.html to see the player analysis visualization

Enter LeBron James, click Analyze, then enter Carmelo Anthony, Add to Analyze, enter Dwyane Wade, Add to Analyze in Player Stats
![Alt text](FinalProject_BackEnd\Data Visualization\PlayerStats.jpg?raw=true "Title")
Enter 2018 in Most Improved Player Stats
![Alt text](FinalProject_BackEnd\Data Visualization\MostImprovedPlayer.jpg?raw=true "Title")
Enter 2018 in Team WinShare
![Alt text](FinalProject_BackEnd\Data Visualization\AllStar.jpg?raw=true "Title")
Select Deep Neural Network in the first dropdown select
![Alt text](DVA_FinalProjectWeb/FinalProject_BackEnd/Data Visualization/AllStar.JPG)
  
## b. Team Evaluation
FinalProject_BackEnd
1. Run Team_Evaluation.Rmd in RStudio to get the evaluation result as well as visualiztion
![Alt text](FinalProject_BackEnd\Data Visualization\Box Plot for pts.jpg?raw=true "Title")
![Alt text](FinalProject_BackEnd\Data Visualization\categories for games.jpg?raw=true "Title")
![Alt text](FinalProject_BackEnd\Data Visualization\Correlation for Important factors.jpg?raw=true "Title")
![Alt text](FinalProject_BackEnd\Data Visualization\Line Charts.jpg?raw=true "Title")
![Alt text](FinalProject_BackEnd\Data Visualization\Plot - Decistion Tree.jpg?raw=true "Title")

FinalProject_FrontEnd
1. Run http://localhost:8000/team.html to see all team analysis visualization 

## c. Champion Evaluation
FinalProject_BackEnd
1. Run main_champion.py in Spyder to get the prediction and validation result
![Alt text](FinalProject_BackEnd\Data Visualization\WinProbability1.png?raw=true "Title")
![Alt text](FinalProject_BackEnd\Data Visualization\WinProbability2.png?raw=true "Title")
![Alt text](FinalProject_BackEnd\Data Visualization\PlayoffProbability.png?raw=true "Title")
![Alt text](FinalProject_BackEnd\Data Visualization\ROCCurve.png?raw=true "Title")
![Alt text](FinalProject_BackEnd\Data Visualization\Precision-Recall.png?raw=true "Title")


FinalProject_FrontEnd
1. Run http://localhost:8000/ChampionPrediction.html or http://localhost:8000/champion.html to see the champion prediction visualization 
![Alt text](FinalProject_BackEnd\Data Visualization\Champion.png?raw=true "Title")
