library(readr)
library(ggplot2)
library(stargazer)
library(lme4)
library(MuMIn)
library(lmerTest)
library(rms)
library(sjstats)
library(ggpubr)

# Importing dataset
data <- read.csv("RDD-ALLProjects.csv",sep=";")
data['time'] <- lapply(data['time'] , factor)

data["month_index"] <- NA
data$month_index <- rep((-12:12)[-12:12 != 0], 285)
data$month_index <- factor(data$month_index, levels=c((-12:12)[-12:12 != 0]),ordered=TRUE)

g1 <- ggplot(data, aes(data$month_index, as.numeric(data$issues_per_month+1))) + 
  geom_boxplot() +
  scale_y_log10(breaks = scales::trans_breaks("log10", function(x) 10^x), 
                labels = scales::trans_format("log10", scales::math_format(10^.x))) +
  theme(text = element_text(size = 7)) +
  labs(y="Issues Per Month", x="Month Index")

ggarrange(g1, nrow = 1, ncol = 1)

ggsave("IssuesPerMonth.png", width = 4, height = 2, dpi = 300)

g2 <- ggplot(data, aes(data$month_index, as.numeric(data$pr_per_month+1))) + 
  geom_boxplot() +
  scale_y_log10(breaks = scales::trans_breaks("log10", function(x) 10^x), 
                labels = scales::trans_format("log10", scales::math_format(10^.x))) +
  theme(text = element_text(size = 7)) +
  labs(y="PR per month", x="Month Index")

ggarrange(g2, nrow = 1, ncol = 1)

ggsave("PullsPerMonth.png", width = 4, height = 2, dpi = 300)

# Plot
g3 <- ggplot(data, aes(data$month_index, as.numeric(data$new_users_issues+1))) + 
  geom_boxplot() +
  scale_y_log10(breaks = scales::trans_breaks("log10", function(x) 10^x), 
                labels = scales::trans_format("log10", scales::math_format(10^.x))) +
  theme(text = element_text(size = 7)) +
  labs(y="New Users Issues", x="Month Index")

ggarrange(g3, nrow = 1, ncol = 1)

ggsave("NewUsersIssues.png", width = 4, height = 2, dpi = 300)


g4 <- ggplot(data, aes(data$month_index, as.numeric(data$new_users_pulls+1))) + 
  geom_boxplot() +
  scale_y_log10(breaks = scales::trans_breaks("log10", function(x) 10^x), 
                labels = scales::trans_format("log10", scales::math_format(10^.x))) +
  theme(text = element_text(size = 7)) +
  labs(y="New Users PR", x="Month Index")

ggarrange(g4, nrow = 1, ncol = 1)

ggsave("NewUsersPulls.png", width = 4, height = 2, dpi = 300)


