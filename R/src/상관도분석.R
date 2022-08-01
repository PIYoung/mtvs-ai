dev.off()
install.packages("arules") # 연관분석 패키지 지지도, 신뢰도, 향상도 계산
install.packages("tidyr")
install.packages("arulesViz")

library("arules")
library("tidyr")
library("arulesViz")

getwd()

# txt 또는 csv의 자료셋중 데이터프레임 구조가 아닌 자료
tr <- read.transactions("R/.R연관분석/data/장바구니분석소스.txt", format = "basket", sep = ",") # nolint
# 필수작업은 아님
# sparse matrix => 희소행렬
tr # 4 transactions => 4 rows / 7 items (데이터를 한 개로 합쳐서 unique한 item 생성)
class(tr)
summary(tr)

inspect(tr)
str(tr)
tr@itemInfo
tr@data

image(tr)
colnames(tr)

# 항복별 지지도
itemFrequency(tr)

itemFrequency(tr[, 1:3])
round(itemFrequency(tr) * 100, 1)
order(itemFrequency(tr)) # 지지도의 값을 작은값이 있는 번호부터 나오게함.
order(-itemFrequency(tr))
colnames(tr[, 3]) # 3번째 제목 확인
itemFrequencyPlot(tr, topN = 4, main = "top 4") # top 4

rules <- apriori(tr, parameter = list(supp = 0.1, conf = 0.1)) # 지지도, 향상도 0.1 이상 자료 # nolint
rules
inspect(rules)

# 10개 항목만 보기 앞쪽의 rules에서 10개 미만일 때
# 아래와 같이 1:10을 하면 에러나옴. 본인의 상황에 맞추어서 개수를 작업해야함
inspect(rules[1:10])
inspect(sort(rules, by = "lift")[1:10]) # lift(향상도) 높은순으로 10개

rules <- apriori(tr, parameter = list(supp = 0.25, conf = 0.5)) # 지지도 25%, 신뢰도 50% 이상구간 # nolint
inspect(rules)
inspect(rules[16:17])
# 사과 구매시 치즈를 사지 않을 확률이 33% 있음

inspect(rules[1:10]) # 10개 항목만 보기
inspect(sort(rules, by = "lift")[1:10]) # lift(향상도) 높은순으로 10개

연관결과 <- inspect(sort(rules, by = "lift"))
head(연관결과)
tapply(연관결과$lift, 연관결과$rhs, mean)
subset(연관결과, subset = lift >= 1) # lift(향상도) 값이 1이상인값만 추출
subset(연관결과, subset = lift >= 1 & support >= 0.5) # lift(향상도) 값이 100이상이면서 support(지지도)가 50 이상 # nolint

사과연관분석 <- 연관결과[grep("사과", 연관결과$lhs), ] # lhs 변수에 '사과'가 포함된 자료만 추출
사과_lift_1이상 <- subset(사과연관분석, subset = (lift >= 1)) # lhs 변수에 '사과' 글자 없는 자료만 추출 # nolint
사과_lift_1이상

사과외연관분석 <- 연관결과[-grep("사과", 연관결과$lhs), ]
사과외연관분석

write.csv(사과연관분석, "R/.R연관분석/data/연관분석결과.csv")

rules <- apriori(tr, parameter = list(supp = 0.25, conf = 0.5))
inspect(rules)
plot(rules) # 가로(지지도), 세로(신뢰도), 색상(향상도)
inspect(sort(rules, by = "lift"))

plot(rules, main = "grouped") # 매트릭스차트
# lhs(가로축)-조건(x아이템)과 rhs(세로축)-결과(y아이템)으로 구성한 매트릭스 그래프

plot(rules, method = "graph") # 네트워크차트
# 각규칙별로어떤아이템들이연관되어묶여있는지보여주는네트워크그래프

dvd <- read.csv("R/.R연관분석/data/dvdtrans.csv")
dvd

dvd$Item[dvd$ID == 1]

dvd_list <- split(dvd$Item, dvd$ID)
dvd_list

dvd_trans <- as(dvd_list, "transactions")
dvd_trans
summary(dvd_trans)
image(dvd_trans)

dvd_rules <- apriori(dvd_trans)
summary(dvd_rules)
inspect(dvd_rules)
dvd_rules <- apriori(dvd_trans, parameter = list(support = 0.2, confidence = 0.6)) # nolint
summary(dvd_rules)
inspect(dvd_rules)
plot(dvd_rules)
plot(dvd_rules, method = "grouped")
plot(dvd_rules, method = "graph")
plot(dvd_rules, method = "graph", control = list(type = "items"))
plot(dvd_rules, method = "paracoord", control = list(reorder = TRUE))

buyer <- read.csv("R/.R연관분석/data/구매내역.csv", as.is = TRUE, encoding = "UTF-8")
buyer

buyer$구매항목[buyer$고객명 == "홍길동"]
buyer_list <- split(buyer$구매항목, buyer$고객명)
buyer_list

buyer_tran <- as(buyer_list, "transactions")
buyer_tran

buyer_list <- sapply(buyer_list, unique)

buyer_tran <- as(buyer_list, "transactions")
buyer_tran

summary(buyer_tran)

itemFrequency(buyer_tran)
itemFrequency(buyer_tran[, 1:5]) # 앞에 있는 5건만 조회
itemFrequencyPlot(buyer_tran, support = 0.01, main = "지지도 1% 이상의 항목들")
itemFrequencyPlot(buyer_tran, topN = 5, main = "지지도 상위 top5 항목들")

buyer_rules <- apriori(buyer_tran)

summary(buyer_rules)
