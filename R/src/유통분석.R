install.packages("lubridate")
install.packages("reshape2")

# 구매일자에서 월 정보만 추출하기 위한 lubridate 라이브러리를 설치한다.
library(lubridate)
# 데이터 조작을 위해 reshape2 라이브러리를 설치한다.
library(reshape2)
library(wordcloud)
library(arules)
library(tidyr)
library(arulesViz)
library(ggplot2)
library(plyr)
library(data.table)

dev.off()
setwd("R")
getwd()

Sys.setlocale(category = "LC_CTYPE", locale = "ko_KR.UTF-8")

df <- read.csv(".R연관분석/data/CUST_ORDER_OUTPUT2.utf8.csv", header = TRUE)
head(df, 5)
str(df)
summary(factor(df$SEX))

df <- df[df$SEX != "*", ]
summary(factor(df$SEX))

# 구매일자, 성별, 구매 건수만 추출하여 별도의 데이터 프레임을 만든다.
sex1 <- subset(df, select = c(ORDER_DATE, SEX, QTY))
head(sex1, 5)

# ORDER_DATE 열에 저장되어 있는 날짜를 이용하여 month 함수로 월만 추출해서 month 라는 새로운 열을 추가한다.
sex2 <- cbind(sex1, month = month(sex1$ORDER_DATE))
head(sex2, 5)

# 성별로 구분하여 월별 구매 건수의 총합을 구해서 확인한다.
dcast(sex2, SEX ~ month, value.var = "QTY", sum)

# F나 M 대신 female, male이라고 표시하기 위해서 변환 함수를 만들어서 적용하여 gender라는 열을 추가한다.
change_gender <- function(x) {
  if (x[2] == "M") {
    return("male")
  } else {
    return("female")
  }
}
sex2$gender <- apply(sex2, 1, change_gender)
sex2$gender <- apply(sex2, 2, change_gender)
head(sex2, 5)

# 성별 별로 월별 구매 건수를 누적 막대 그래프로 표시한다.
qplot(month, data = sex2, geom = "bar", fill = gender)

# 성별 별로 월별 구매 건수를 별도의 막대 그래프로 표시한다.
ggplot(sex2, aes(month)) +
  geom_bar() +
  facet_wrap(~gender)


# 연령대 구매 건수
# 구매일자, 나이, 구매 건수 만 추출하여 별도의 데이터 프레임을 만든다.
age1 <- subset(df, select = c(ORDER_DATE, AGE, QTY))
head(age1)

# ORDER_DATE 열에 저장되어 있는 날짜를 이용하여 month 함수로 월만 추출해서 month 라는 새로운 열을 추가한다.
age2 <- cbind(age1, month = month(age1$ORDER_DATE))

# 연령별로 구분하여 월별 구매 건수의 총합을 구해서 확인한다.
dcast(age2, AGE ~ month, value.var = "QTY", sum)

# 그래프에 표시할 때, 10대, 20대, 30대와 같이 표시될 수 있도록 나이에 "대＂를 붙여서 ages라는 열을 추가한다.
age2 <- cbind(age2, ages = paste(age2$AGE, "대"))

# 연령 별로 월별 구매 건수를 누적 막대 그래프로 표시한다.
qplot(month, data = age2, geom = "bar", fill = ages)

# 연령 별로 월별 구매 건수를 별도의 막대 그래프로 표시한다.
ggplot(age2, aes(month)) +
  geom_bar() +
  facet_wrap(~AGE)


# 성별/연령대 구매 건수
# 구매일자, 성별, 나이, 구매 건수만 추출하여 별도의 데이터 프레임을 만든다.
sex_age1 <- subset(df, select = c(ORDER_DATE, SEX, AGE, QTY))
head(sex_age1)

# ddply() 함수를 사용하여 날짜, 성별, 나이로 그룹을 지어 구매 수량을 합쳐서 확인한다.
sex_age2 <- ddply(
  sex_age1,
  .(ORDER_DATE, SEX, AGE),
  summarize,
  Sum_F = sum(QTY)
)
head(sex_age2)

# month() 함수로 월만 추출하여 month 열을 추가하고, ages 열에는 나이에 "대＂를 붙여서 추가한다.
sex_age3 <- cbind(sex_age2, month = month(sex_age2$ORDER_DATE))
sex_age3 <- cbind(sex_age3, ages = paste(sex_age3$AGE, "대"))
head(sex_age3)

# 성별과 연령을 기준으로 월별 구매 건수를 별도의 막대 그래프로 표시한다.
ggplot(sex_age3, aes(month)) +
  geom_bar() +
  facet_wrap(~ SEX + ages)

# 연령대/성별 구매 건수
# ddply() 함수를 사용하여 날짜, 나이, 성별로 그룹을 지어 구매 수량을 합쳐서 확인한다.
sex_age2 <- ddply(
  sex_age1,
  .(ORDER_DATE, AGE, SEX),
  summarise,
  Sum_F = sum(QTY)
)

# month() 함수로 월만 추출하여 month 열을 추가하고, ages 열에는 나이에 "대＂를 붙여서 추가한다.
sex_age3 <- cbind(sex_age2, month = month(sex_age2$ORDER_DATE))
sex_age3 <- cbind(sex_age3, ages = paste(sex_age3$AGE, "대"))

# 연령과 성별을 기준으로 월별 구매 건수를 별도의 막대 그래프로 표시한다.
ggplot(sex_age3, aes(month)) +
  geom_bar() +
  facet_wrap(~ ages + SEX)

# 월별 고객단위 구매금액
# 구매일자, 고객 번호, 구매 금액 만 추출하여 별도의 데이터 프레임을 만든다.
cust1 <- subset(df, select = c(ORDER_DATE, CUST_SERIAL_NO, PRICE))
head(cust1)

# month() 함수로 월만 추출하여 month 열을 추가한다.
cust2 <- cbind(cust1, month = month(cust1$ORDER_DATE))
nrow(cust2)

# ddply() 함수를 사용하여 고객 번호와 월로 그룹을 지어 구매 금액을 합쳐서 확인한다.
cust3 <- ddply(
  cust2,
  .(CUST_SERIAL_NO, month),
  summarize,
  Sum_F = sum(PRICE)
)
nrow(cust3)
head(cust3)

# aggregate() 함수를 이용하여 고객 번호와 월을 기준으로 구매 금액을 합친다.
df2 <- cbind(df, month = month(df$ORDER_DATE))
agg_data <- aggregate(PRICE ~ CUST_SERIAL_NO + month, data = df2, sum)

# 그래프의 범례로 사용하기 위해 월에 "월＂을 붙여서 real_month라는 열을 추가한다.
agg_data <- cbind(agg_data, real_month = paste(agg_data$month, "월"))
head(agg_data)

# 월별 총 구매 금액의 최대값과 최소값, 평균값 등을 비교하기 위해 상자 차트로 표시한다.
p <- ggplot(agg_data, aes(real_month, PRICE))
p + geom_boxplot(aes(fill = real_month))

# 500,000원 미만으로 Filter
# 구매 금액의 총합이 50만원 미만인 고객을 추출하여 고객 수를 확인한다.
str(cust3)
cust4 <- subset(cust3, Sum_F < 500000)
nrow(cust4)

# 월별 총 구매 금액이 50만원 미만인 구매에 대해서 최대값과 최소값, 평균값 등을 비교하기 위해 상자 차트로 표시한다.
p <- ggplot(
  subset(
    agg_data,
    PRICE < 500000
  ),
  aes(real_month, PRICE)
)
p + geom_boxplot(aes(fill = real_month))

# 요일별 구매 금액 합계
# 구매 요일, 구매 건수만 추출하여 별도의 데이터 프레임을 만든다.
day1 <- subset(df, select = c(ORDER_WEEKDAY, PRICE))
head(day1)

# ddply() 함수를 사용하여 요일별로 구매 금액을 합쳐서 확인한다.
day2 <- ddply(day1, .(ORDER_WEEKDAY), summarize, Sum_F = sum(as.numeric(PRICE)))
day2

# ddply() 함수를 사용하여 요일별로 구매 금액을 합친 결과를 agg_data_summary에 저장한다.
agg_data_summary <- ddply(
  day1,
  .(ORDER_WEEKDAY),
  summarize,
  Sum_F = sum(as.numeric(PRICE))
)

# 그래프에 출력될 때 자동으로 정렬해서 출력되도록 요일 앞에 1부터 7까지의 숫자를 붙이는 함수를 만들어서 적용한다.
change_r_day <- function(x) {
  if (length(grep(x[1], "월")) > 0) {
    return("1_월")
  } else if (length(grep(x[1], "화")) > 0) {
    return("2_화")
  } else if (length(grep(x[1], "수")) > 0) {
    return("3_수")
  } else if (length(grep(x[1], "목")) > 0) {
    return("4_목")
  } else if (length(grep(x[1], "금")) > 0) {
    return("5_금")
  } else if (length(grep(x[1], "토")) > 0) {
    return("6_토")
  } else if (length(grep(x[1], "일")) > 0) {
    return("7_일")
  }
}
agg_data_summary$rday <- apply(agg_data_summary, 1, change_r_day)
agg_data_summary

# 요일별 구매 금액의 총합을 막대 그래프로 표시한다.
ggplot(agg_data_summary, aes(rday, Sum_F)) +
  geom_bar(stat = "identity")

# 요일별 구매 상품 수
# ddply() 함수를 사용하여 요일별로 구매 수량을 합친 결과를 day_amt2에 저장하고, 요일 이름 변경 함수를 적용하여 rday 열을 추가한다. # nolint
day_amt1 <- subset(df, select = c(ORDER_WEEKDAY, QTY))
day_amt2 <- ddply(day_amt1, .(ORDER_WEEKDAY), summarize, Sum_F = sum(QTY))
day_amt2$rday <- apply(day_amt2, 1, change_r_day)
day_amt2

# 요일별 총 구매 수량이 2개를 초과하는 구매에 대해서 최대값과 최소값, 평균값 등을 비교하기 위해 상자 차트로 표시한다.
p <- ggplot(subset(df, QTY > 2), aes(ORDER_WEEKDAY, QTY))
p + geom_boxplot(aes(fill = ORDER_WEEKDAY))

# 전체 고객의 구매수량 상위 100개의 세 분류 상품에 대하여 wordcloud 표현
# 상품 분류 코드와 구매 수량 데이터만 추출한 다음 동일한 상품 분류 코드에 대한 누적 구매 수량을 구한다.
dgroup1 <- subset(df, select = c(LGROUP, MGROUP, SGROUP, DGROUP, QTY))
head(dgroup1)
dgroup2 <- ddply(dgroup1,
  .(LGROUP, MGROUP, SGROUP, DGROUP),
  summarize,
  Sum_F = sum(QTY)
)
head(dgroup2)
nrow(dgroup2)

# 조인을 하기 위해서, 4개의 상품 분류 코드를 하나의 문자열로 합친 다음 LMSD_ICODE 열에 저장한다.
dgroup2 <- cbind(
  dgroup2,
  LMSD_ICODE = paste(
    dgroup2$LGROUP,
    "|",
    dgroup2$MGROUP,
    "|",
    dgroup2$SGROUP,
    "|",
    dgroup2$DGROUP
  )
)

# 상품 분류 코드에 따른 분류 이름이 저장된 CSV 파일을 읽은 다음, 역시 조인을 하기 위해서, 4개의 상품 분류 코드를 하나의 문자열로 합친 다음 LMSD_ICODE 열에 저장한다. # nolint
vhd <- read.csv(".R연관분석/data/VHD_GOODSKIND.csv", header = TRUE)
vhd <- cbind(vhd,
  LMSD_ICODE = paste(
    vhd$LGROUP,
    "|",
    vhd$MGROUP,
    "|",
    vhd$SGROUP,
    "|",
    vhd$DGROUP
  )
)

# 두 개의 데이터 프레임을 LMSD_ICODE 열을 기준으로 조인하여 합치고 구매수량 기준으로 내림차순 정렬을 한다.
vhd2 <- subset(
  vhd,
  select = c(LMSD_ICODE, DGROUP_NAME)
)
dgroup2 <- merge(
  x = dgroup2,
  y = vhd2,
  by = "LMSD_ICODE",
  all = TRUE
)
dgroup3 <- dgroup2[c(order(-dgroup2$Sum_F)), ]
head(dgroup3)

# dgroup3에서 상위 100개의 합계만 추출하여 별도의 벡터로 만든다.
vec1 <- c()
for (j in 1:100) {
  print(j)
  print(dgroup3$Sum_F[j])
  vec1 <- c(vec1, as.numeric((dgroup3$Sum_F[j])))
}
vec1

# wordcloud를 이용하여 상위 100개의 상품 세 분류 이름을 시각화 한다.
palette <- brewer.pal(9, "Set1")
wordcloud(dgroup3$DGROUP_NAME,
  vec1,
  scale = c(5, 1),
  rot.per = 0.25,
  min.freq = 2,
  random.order = FALSE,
  random.color = TRUE,
  colors = palette
)

# 연관성 분석을 통한 상품 추천
# 구매 내역 중 "패션/잡화"와 "뷰티" 대분류에 대한 연관성을 분석한다.
# LGROUP이 10(패션/잡화)이거나 20(뷰티)인 항목을 추출하여 anal_df에 저장한다. 고객 번호와 구매 월, 구매 요일을 이용하여 ID를 생성하고 조인을 위해 LMSD_ICODE도 추가한다.  # nolint
anal_df <- subset(df, LGROUP == c(10, 20))
anal_df <- cbind(anal_df, month = month(anal_df$ORDER_DATE))
anal_df$ID <- paste(
  anal_df$CUST_SERIAL_NO,
  anal_df$month,
  anal_df$ORDER_WEEKDAY,
  ㅠsep = "_"
)
anal_df <- cbind(anal_df,
  LMSD_ICODE = paste(
    anal_df$LGROUP,
    "|",
    anal_df$MGROUP,
    "|",
    anal_df$SGROUP,
    "|",
    anal_df$DGROUP
  )
)
anal_df <- merge(x = anal_df, y = vhd2, by = "LMSD_ICODE", all = TRUE)
str(anal_df)

# 분석을 위한 변수들을 선택한다.
anal_df <- anal_df[, c("ID", "DGROUP_NAME")]
str(anal_df)
# 연관성 분석을 위해서 리스트 형식으로 변환 한다.
uni_id <- unique(anal_df$ID)
uni_id
list_x <- data.table(anal_df)
list_x <- list_x[, unique(DGROUP_NAME), by = ID]
list_x <- data.frame(list_x[, lapply(.SD, list), by = ID])
list_x <- list_x[, 2]
names(list_x) <- paste("Tr", c(seq_along(uni_id)), sep = "")

# 대용량의 데이터로부터 효율적으로 연관 규칙을 도출하기 위해 사용하는 arules 패키지를 설치한다.
arules_list <- as(list_x, "transactions")
list_x[1:10]
# apriori() 함수를 사용하여 연관성 분석을 수행한다. 분석 결과를 적절하게 도출하려면 support 값과 confidence 값을 조절하면서 분석을 수행해야 한다. # nolint
arules_result <- apriori(arules_list,
  parameter = list(
    supp = 0.0001,
    confidence = 0.0001
  )
)

# 78개의 룰에 대한 분석 결과를 시각화 한다.
plot(arules_result)

# 패션/잡화와 뷰티가 어떻게 연관되어 있는지 상세히 표시한다.
plot(arules_result, method = "grouped")

# 각 상품에 대한 연관성을 관계도를 이용하여 보여준다. 이를 통해서 대분류별 1회 구매 시에 구매 특성을 알 수 있다.
plot(arules_result, method = "graph", control = list(type = "items"))

# 연관성 분석 결과를 CSV 파일로 저장한다.
write.csv(as(
  arules_result,
  "data.frame"
),
"result.csv",
row.names = FALSE
)


# 등산화 한가지 분류에 대한 룰을 선택하여 시각화
# 연관성 분석을 수행한 결과 만들어지는 arules_result에서 등산화 관련 부분만 추출한다.
test <- subset(arules_result, subset = rhs %in% "등산화")

# 반팔이나 바지를 구매한 고객은 등산화도 같이 구매하는 연관성을 도출했다. 따라서, 향후 고객들이 반팔이나 바지를 구매할 때 등산화 구매를 추천해줄 수 있다. # nolint
plot(test, method = "graph", control = list(type = "items"))

# markdown
# #연관성 분석
# - 연관성 분석이란 "연관 규칙(Association Rule)"을 발견하는 과정을 말한다.
# - 여기서 말하는 연관 규칙은 상품을 구매하는 행위에 대한 연관성에 대한 규칙을 뜻하며
# - 고객이 구매하는 장바구니에 들어있는 품목간의 관계를 분석하기 때문에
# - "장바구니 분석(Market Basket Analysis)"라고도 부른다.

# - 연관성 분석을 하는 이유는
#   - 특정한 상품을 구입한 고객이 어떤 그룹에 속하는지를 파악하기 위해서이다.
# - 이러한 연관성 분석을 활용하면 매장 내에 효율적으로 상품을 진열할 수 있고
# - 패키지 상품을 개발하는데 도움이 되며 교차 판매 전략을 구사하거나 기획 상품을 결정할 수 있다.
# - 즉, 연관성 분석의 목적은 유용한 규칙을 찾고 유용한 규칙에 대한 확률을 계량화하여 표현하는데 있다고 볼 수 있다.

# - 연관성 규칙은 다음과 같은 종류의 규칙으로 분류될 수 있다.
#   - 유용한 규칙: 목요일에 마트를 찾는 고객은 아기 기저귀와 맥주를 같이 구입하는 경향이 있다.
#   - 자명한 규칙: 특정 회사의 전자 제품을 구매하는 고객은 새로운 전자 제품을 구매할 때 같은 회사의 제품을 구입하는 경향이 있다.
#   - 설명이 불가능한 규칙: 새로 문을 연 건축자재 판매점에서는 변기 덮개가 많이 팔리는 경향이 있다.
