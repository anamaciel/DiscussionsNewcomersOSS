library(ggplot2)
library(tidyverse)

#comments+replies

dataCommentsReplies <- read.csv("C:/Users/anacm/Documents/DOUTORADO/GITHUB/Scripts/2024/PacoteReplicacao/RQ1/commentsRepliesPerROLEPercent.csv",sep=",",encoding = "iso-8859-3")

boxplot((dataCommentsReplies))

median(dataCommentsReplies$Core.developers)
median(dataCommentsReplies$Peripheral.developers)
median(dataCommentsReplies$Issues.reporters)
median(dataCommentsReplies$Discussions.contributors)

dataCommentsReplies_melt <- pivot_longer(dataCommentsReplies,names_to="groups",values_to="count",cols=1:4)
modelCommentsReplies <- lm(count~groups,dataCommentsReplies_melt)
summary(modelCommentsReplies)
anova(modelCommentsReplies)
ems <- emmeans::emmeans(modelCommentsReplies,pairwise~groups)
ems

emmeans::eff_size(ems, method="pairwise",edf = df.residual(modelCommentsReplies),sigma = sigma(modelCommentsReplies))

#discussions

dataDiscussions <- read.csv("C:/Users/anacm/Documents/DOUTORADO/GITHUB/Scripts/2024/PacoteReplicacao/RQ1/discussionsPerROLEPercent.csv",sep=",",encoding = "iso-8859-3")

boxplot((dataDiscussions))

median(dataDiscussions$Core.developers)
median(dataDiscussions$Peripheral.developers)
median(dataDiscussions$Issues.reporters)
median(dataDiscussions$Discussions.contributors)

dataDiscussions_melt <- pivot_longer(dataDiscussions,names_to="groups",values_to="count",cols=1:4)
modelDiscussions <- lm(count~groups,dataDiscussions_melt)
summary(modelDiscussions)
anova(modelDiscussions)
ems <- emmeans::emmeans(modelDiscussions,pairwise~groups)
ems

emmeans::eff_size(ems, method="pairwise",edf = df.residual(modelDiscussions),sigma = sigma(modelDiscussions))


#distribuição dos grupos por role

userPerRole <- read.csv("C:/Users/anacm/Documents/DOUTORADO/GITHUB/Scripts/2024/PacoteReplicacao/RQ1/quantityUsersPerRole-v2.csv",sep=";",encoding = "iso-8859-3")

boxplot(log(userPerRole))


