setwd("C:/Users/Tyson/Desktop/")
data <- read.csv(file="SentimentOut_v2.txt",sep=",",header=F)
names(data) <- c("text","textlength","ups","avgpol","medpol","lqpol","uqpol","modeword","modecount","minpol","maxpol","avgsubj","medsubj","lqsubj","uqsubj","minsubj","maxsubj")
View(data)
plot(data$ups,data$textlength)
plot(data$textlength,data$avgpol) +
plot(data$textlength,data$maxpol)

data$log <- log(data$textlength)

library(ggplot2)

ggplot(data) + geom_point(aes(x=textlength,y=maxpol),color="Green") +
  geom_point(aes(x=textlength,y=minpol),color="Red") +
  geom_point(aes(x=textlength,y=avgpol),color="Blue")

length(unique(data$text))

length(data$maxsubj)
length(data$minsubj)
length(data$avgsubj)
plot(data$V4,data$V2)

# library(dplyr)
# install.packages("zoo")
# library(zoo)

# 
# train <- data.frame(D = 1:3)
# full.dates <- as.Date(min(as.Date("2011-01-01")):max(as.Date("2015-01-01")), origin = "1970-01-01")
# db <- data.frame(Date = full.dates)
# fixed <- left_join(db, train)
# 
# # Fill from top using zoo::na.locf
# fixed[ ,c("D", "S")] <- na.locf(fixed[ ,c("D", "S")])
# fixed
# 
# train <- data.frame(D = 1:3, S = 4:6, Date = as.Date("2010-02-05") + 7*(1:3))
# full.dates <- as.Date(min(train$Date):max(train$Date), origin = "1970-01-01")
# db <- data.frame(Date = full.dates)
# fixed <- left_join(db, train)
# 
# # Fill from top using zoo::na.locf
# fixed[ ,c("D", "S")] <- na.locf(fixed[ ,c("D", "S")])
