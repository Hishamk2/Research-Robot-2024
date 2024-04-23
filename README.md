This repo includes all data sets and scripts used in "Developers Discussions on Robotics: A First Look", including a data set of all questions on Stack overflow matching the
"robot" and "robots" tag, a subset of 301 of those questions, 225 coded robot questions,  a dataset of over one million random questions from Stack Overflow, and a dataset of
over one million random answers from Stack Overflow. It is expected that the robot dataset will be useful for future work, as such, details are given about this dataset below:



Dataset of robot questions and answers on Stack Overflow between August 1, 2008 and March 27, 2024 (extracted April 3 2024).

Includes: 
Question Id,
Question Title,
Tags,
Question Body,
Question Creation Date,
Accepted Answer Id, Question View Count,
Answer Count,
Comment Count,
Question Score,
Question Favourite Count*,
Question Asker User Id,
Question Asker User Location,
Question Asker User Creation Date,
Question Asker User Views,
Answer Id,
Answer Body,
Answer User Id,
Answer Score,
Answer Comment Count

For questions with multiple answers and/or multiple comments, the question will appear in multiple rows in the data set with a different answer in the answer columns for
each entry of that question. Each combination of question and answer is again repeated for each comment. 
For example, if a question has three answers, and two comments, there will be six rows
in the data set with the same question ID and associated question data, three rows with the first comment and different data associated with each answer in each row,
and three rows with the second comment and the data associated with answers being different in each row.

*Question Favourites appears to no longer be supported by Stack Overflow, and is 0 or empty for every row
