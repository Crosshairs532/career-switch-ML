# Introduction

This project aims to classify whether a person will change his/her current job. The dataset contains information about the candidate's previous job history. Now let’s say we want to hire a candidate and train them. But it would be efficient to know whether after training a person will stay on their current job or not. It would save time and cost as well as the planning and categorizing the candidates. However, to reduce the burden of this work load, we are trying to create a machine learning model that would ease our work and predict whether a candidate will continue his/her job or not. 

# Dataset Description
This Dataset contains information about 5000 people and 12 features. It includes where they live and how developed the cities are. It also contains information about the people's educational disciplines, their working places, salaries, work experience and how often a person changes his/her jobs or at least when last changed a job. Along with that what type of company he/she was working on. Our Dataset contains both numerical and categorical data. In some features, there is some mixed data. Lastly,  based on this information,  our goal is to determine whether a person will change his/her jobs. So, it signifies a classification problem, as it is given us only a yes or no answer. 

# Dataset pre-processing: 


- Missing Values: 

To handle categorical data we imputed the missing values with the most frequent values from the rows in a specific column. As the number of missing values were huge, we deceived to impute instead of removing the rows. 

	
To handle numerical data we were aware of while imputing. To keep the actual distribution of a specific column, we checked using the mean, median , mode imputation. We have seen that in most columns using mode was better and it gave the actual columns distribution. 

- Encoding:

To handle categorical values, we  first identify the column that has ordinality in the column. Those who had ordinality in the column, for them we used Ordinal Encoder, and for the others we used OneHotEncoding. For example, to deal with the “gender” column we use one hot encoding. On the other hand, to deal with the “education level” column we used ordinal encoding.

- Skewed Data:

We saw that some of our data did not have any normal distribution. Some models like logistic regression perform well in normally distributed data. And so to solve this issue, we used function transformation like power transformation named yeo-johnson to make the distribution normalised and to reduce skewness.

- Feature Scaling:

There were some columns that were in different units. And  each unit would represent a different meaning. so to keep the weights of each column the same we used normalised scaling. Mainly we used MinMaxScaler. 

- Outlier:

We saw some of our features had outliers like ‘company size”. Usually outliers had a negative impact on models while training. And so we used methods like IQR as it worked the best to remove the outliers from the data.
