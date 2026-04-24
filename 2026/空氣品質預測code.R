# ================================
# 1. 安裝/載入套件
# ================================
# install.packages("ranger")
library(ranger)

# ================================
# 2. 讀取資料
# ================================
train <- read.csv("train.csv")
test  <- read.csv("test.csv")

# ================================
# 3. 處理類別變數
# ================================
train$Country <- as.factor(train$Country)
train$City    <- as.factor(train$City)

test$Country <- factor(test$Country, levels = levels(train$Country))
test$City    <- factor(test$City, levels = levels(train$City))

train$AQI.Category <- as.factor(train$AQI.Category)

# ================================
# 4. 訓練 / 驗證集切分
# ================================
set.seed(42)
train_idx <- sample(1:nrow(train), 0.8 * nrow(train))

train_data <- train[train_idx, ]
valid_data <- train[-train_idx, ]

# ================================
# 5. 訓練 ranger 隨機森林
# ================================
model <- ranger(
  formula = AQI.Category ~ .,
  data = train_data,
  num.trees = 400,
  mtry = 4,
  probability = FALSE
)

# ================================
# 6. 驗證準確率
# ================================
valid_pred <- predict(model, valid_data)$predictions
valid_pred <- factor(valid_pred, levels = levels(train$AQI.Category))

accuracy <- mean(valid_pred == valid_data$AQI.Category)
cat("Validation Accuracy:", accuracy, "\n")

# ================================
# 7. Test 預測
# ================================
test_pred <- predict(model, test)$predictions

# ================================
# 8. 文字 → 數字對照表
# ================================
label_map <- c(
  "Good" = 1,
  "Moderate" = 2,
  "Unhealthy for Sensitive Groups" = 3,
  "Unhealthy" = 4,
  "Very Unhealthy" = 5,
  "Hazardous" = 6
)

# 如果 test_pred 是 factor/文字，轉成數字
test_pred_num <- label_map[as.character(test_pred)]

# ================================
# 9. 輸出 submission.csv
# ================================
submission <- data.frame(
  index = test$index,
  AQI.Category = test_pred_num
)

write.csv(submission, "412421446.csv", row.names = FALSE)
cat("✔ submission.csv 已產生（AQI.Category 已轉為數字 1~6），可以直接上傳 Kaggle！\n")
