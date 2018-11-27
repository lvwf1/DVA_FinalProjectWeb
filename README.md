# DVA_FinalProjectWeb

### DESCRIPTION
The project is completed by CSE6242 Data Visual Analytics Team80 for the topic of NBA Players and Teams Analysis.
Team Members: Zibin Chen, Weifeng Lyu, Zeyu Ni, Jingya Qin, Jian Zhan, Yang Zhang

### INSTALLATION
Prerequisite: Python 3.6, Pycharm IDE, RStudio, Spyder
Required Packages for Python 3.6: flask, flask_restful, flask_cors, pandas, numpy, matplotlib, sklearn, keras, tensorflow, collections

Clone this repository, Import <path>/FinalProject_BackEnd project files into PyCharm Project with Flask Template with Default Settings, install All required packeages to python virtual environment
  
  OR
  
Open Terminal, pip all required packeages in terminal

### EXECUTION
## a. Player Evaluation
FinalProject_BackEnd:
1. Run DVA_FinalProjectWeb in PyCharm directly OR Use PyCharm Terminal then enter command: python.exe -m flask run
2. The back-end application is running localhost under http://localhost:5000/ by default

  OR
  
1. cd <path>/FinalProject_BackEnd, python.exe -m flask run
2. The back-end application is running localhost under http://localhost:5000/ by default

FinalProject_FrontEnd:
1. Open Terminal, cd <path>/FinalProject_FrontEnd
2. python -m http.server
3. The front-end application is running localhost under http://localhost:8000/ by default
4. Run http://localhost:8000/player.html to see the player analysis visualization

Enter LeBron James, click Analyze, then enter Carmelo Anthony, Add to Analyze, enter Dwyane Wade, Add to Analyze in Player Stats
![playerstats](https://user-images.githubusercontent.com/34119702/49113184-27685d00-f295-11e8-9904-9f5cb16eaa3b.JPG)

Enter 2018 in Most Improved Player Stats
![mostimprovedplayer](https://user-images.githubusercontent.com/34119702/49113207-33ecb580-f295-11e8-938a-39cb49686b0b.JPG)

Enter 2018 in Team WinShare
![teamwinshare](https://user-images.githubusercontent.com/34119702/49113230-4535c200-f295-11e8-9991-b894a03ea78d.JPG)

Select Deep Neural Network in the first dropdown select
![allstar](https://user-images.githubusercontent.com/34119702/49113145-0acc2500-f295-11e8-9e1f-059b9b683116.JPG)
  
## b. Team Evaluation
FinalProject_BackEnd
1. Run Team_Evaluation.Rmd in RStudio to get the evaluation result as well as visualiztion
<img width="969" alt="box plot for pts" src="https://user-images.githubusercontent.com/34119702/49113248-54b50b00-f295-11e8-8611-2e0dde0a6d36.png">
<img width="967" alt="categories for games" src="https://user-images.githubusercontent.com/34119702/49113297-77dfba80-f295-11e8-9541-1afa1cfae6f8.png">
<img width="728" alt="correlation for important factors" src="https://user-images.githubusercontent.com/34119702/49113311-8332e600-f295-11e8-8503-1f10e84dc750.png">
<img width="959" alt="line charts" src="https://user-images.githubusercontent.com/34119702/49113334-8cbc4e00-f295-11e8-8afc-fb6f368c1089.png">
<img width="401" alt="plot - decistion tree" src="https://user-images.githubusercontent.com/34119702/49113351-9d6cc400-f295-11e8-8ab1-acd0e5223489.png">

FinalProject_FrontEnd
1. Run http://localhost:8000/team.html to see all team analysis visualization 

## c. Champion Evaluation
FinalProject_BackEnd
1. Run main_champion.py in Spyder to get the prediction and validation result
![winprobability1](https://user-images.githubusercontent.com/34119702/49113362-a9f11c80-f295-11e8-8d49-ce0ca2c0eb7f.png)
![winprobability2](https://user-images.githubusercontent.com/34119702/49113375-b2495780-f295-11e8-84be-d3388be4a95d.png)
![playoffprobability](https://user-images.githubusercontent.com/34119702/49113393-bf664680-f295-11e8-952d-0e9a8c575792.png)
![roccurve](https://user-images.githubusercontent.com/34119702/49113410-c8571800-f295-11e8-9666-c5191912239c.png)
![precision-recall](https://user-images.githubusercontent.com/34119702/49113431-d311ad00-f295-11e8-8d22-6412e83f6da8.png)


FinalProject_FrontEnd
1. Run http://localhost:8000/ChampionPrediction.html or http://localhost:8000/champion.html to see the champion prediction visualization 
![Alt text](FinalProject_BackEnd\Data Visualization\Champion.png?raw=true "Title")
