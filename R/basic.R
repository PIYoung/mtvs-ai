# R에서의 데이터프레임 인덱싱 객체명$필드명 혹은 객체명[행, 열]
mtcars$mpg
mtcars$mpg[3:5]
mtcars # 내장 데이터 불러오기
str(mtcars) # 내장 데이터 구조 (파이썬 info)
summary((mtcars)) # 판다스의 describe와 같음

plot(mtcars)
boxplot(mtcars)
barplot(mtcars$mpg, mtcars$hp)

# 값을 unique하게 만든 후 count하여서 막대 차트 그리기
barplot(table(mtcars$cyl))
barplot(table(mtcars[, 2])) # 위랑 같음
barplot(table(mtcars$disp))
mtcars[, 1] # 첫 번째 열 보기
mtcars$mpg

data()
str(AirPassengers)
as.data.frame(AirPassengers)

# R에서는
# 문자열을 character와 factor로 나눔
# factor는 카테고리별 count가 기본제공, split 안됨
# => 카테고리를 레이블(라벨)이라 칭하고
#    라벨의 순서를 변경할 수 있음
#    (서울, 대전, 부산) => (대전, 부산, 서울)
# character는 count제공안됨, split됨

# r에서는 2개이상의 스칼라는 c로
# 파이썬에[1, 2, 3, 4, 5]와 같음
x <- c(1, 2, 3, 4, 5, 2, 3, 1, 2, 3, 2, 9)
str(x)
summary(x)

x2 <- factor(x, levels = c(1, 2, 3, 4))
summary((x2))

plot(x)
plot(x2)

score <- c(92, 90, 82, 88, 78, 64, 82, 90)
subject <- c("k", "k", "m", "m", "m", "m", "k", "k")
# factor는 split 불가능
sub <- as.factor(subject)
tmp <- strsplit(subject, "")
tmp

summary(score)
table(subject)
summary(sub)

getwd()

키 <- c(167, 172, 182, 169)
체중 <- c(78, 72, 88, 54)
나이 <- c(29, 24, 25, 21)
students <- data.frame(키, 체중, 나이)

str(students)
summary(students)
boxplot(students)
boxplot(scale(students))
summary(scale(students))

# psych 패키지 이용해보기
install.packages("psych")
library("psych")

pairs.panels(students, stars = TRUE, lm = TRUE)
steam(students$키)
students$키
