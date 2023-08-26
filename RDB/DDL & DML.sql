# DDL
CREATE TABLE Athlete (
    athlete_id INT PRIMARY KEY,
    name VARCHAR(255),
    sex CHAR(1),
    age INT
);
CREATE TABLE Team (
    team_id INT PRIMARY KEY,
    team_name VARCHAR(255),
    NOC VARCHAR(255)
);
CREATE TABLE Game (
    game_id INT PRIMARY KEY,
    year INT,
    season VARCHAR(255),
    city VARCHAR(255)
);
CREATE TABLE Participation (
    participation_id INT NOT NULL AUTO_INCREMENT, -- surrogate key
    athlete_id INT NOT NULL,
    game_id INT NOT NULL,
    PRIMARY KEY (participation_id),
    FOREIGN KEY (athlete_id) REFERENCES Athlete(athlete_id),
    FOREIGN KEY (game_id) REFERENCES Game(game_id)
);

# DML
INSERT INTO Athlete (athlete_id, name, sex, age, team_id)
VALUES 
    (1, 'Michael Johnson', 'M', 25, 1),
    (2, 'Dan Jansen', 'M', 28, 1),
    (3, 'Bonnie Blair', 'F', 29, 1),
    (4, 'Oksana Baiul', 'F', 16, 2)
;
INSERT INTO Team (team_id, team_name, NOC)
VALUES 
    (1, 'United States', 'USA'),
    (2, 'Russia', 'RUS'),
    (3, 'Germany', 'GER'),
    (4, 'Norway', 'NOR')
;
INSERT INTO Game (game_id, year, season, city)
VALUES 
    (1, 1992, 'Summer', 'Barcelona'),
    (2, 1994, 'Winter', 'Lillehammer'),
    (3, 1996, 'Summer', 'Atlanta'),
    (4, 1998, 'Winter', 'Nagano')
;
INSERT INTO Participation (athlete_id, game_id)
VALUES 
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 2)
;
