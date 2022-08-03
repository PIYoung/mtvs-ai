install.packages("wordcloud")
install.packages("extrafont")

library("wordcloud")
library("arules")
library("tidyr")
library("arulesViz")
library(extrafont)
library(remotes)

dev.off()

word <- c("python", "corona", "park")
cnt <- c(20, 40, 50)
df <- data.frame(단어 = word, 빈도수 = cnt)
df

wordcloud(df$단어, df$빈도수, rot.per = 0, min.freq = 5, colors = "blue")

df <- read.csv("R/data/1news.csv", sep = ",", header = TRUE)
head(df)
str(df)
names(df) # 변수명만 추출, 판다스의 colnames
unique(df$언론사)

field_filter <- data.frame(
  언론사 = df$언론사,
  기사 = df$특성추출.가중치순.상위.50개.
)
typeof(grep("한겨레", field_filter$언론사))
grep("한겨레", field_filter$언론사)
grep("매일신문", field_filter$언론사)
grep("중앙일보", field_filter$언론사)
한겨레 <- field_filter[grep("한겨레", field_filter$언론사), ]
매일신문 <- field_filter[grep("매일신문", field_filter$언론사), ]
중앙일보 <- field_filter[grep("중앙일보", field_filter$언론사), ]
dim(한겨레)
dim(매일신문)
dim(중앙일보)

# 차트여백
par("mar")
par(mar = c(1, 1, 1, 1))

tmp <- grep("매일신문", df$언론사)
barplot(table(tmp$일자))
summary(df$일자)
summary(table(df$일자))

# 워드클라우드를 하려면 단어별 빈도수를 제작
# 지금자료는 기사에 쉼표단위로 문장이 있어엇
# 쉼표단위로 데이터를 나눔
# R에서는 split을 하면 리스트구조가 됨
# 1번자료 split 자료, 2번자료 split 자료
# split된 리스트 자료를 한개의 변수로 합쳐야함
# 파이썬에서는 이 기능을 join함수로
split <- strsplit(한겨레$기사, ",")
split[[2]]
unlist <- unlist(split)
unlist
result <- table(unlist)
result
barplot(result)

extrafont::font_import(
  # path = "C:/Users/HP/AppData/Local/Microsoft/Windows/Fonts",
  # path = "C:/Windows/Fonts",
  path = "C:/Users/HP/AppData/Local/Temp/RtmpM3SJhC/fonts",
  pattern = "malgun.ttf",
  prompt = FALSE
)
loadfonts(device = "win")
windowsFonts(malgun = windowsFont("malgun"))
fonts()
warnings()

list.files("C:/Windows/Fonts") # TRUE
file.exists("C:/Windows/Fonts/malgun.ttf")

par(bg = "white") # 배경색 검정
display.brewer.all() # 색상표 출력
pal <- brewer.pal(7, "Set3")

wordcloud(names(result),
  result,
  rot.per = 0,
  min.freq = 1,
  random.order = FALSE,
  family = "D2Coding",
  color = pal
)
warnings()

tmp <- data.frame(result)
write.csv(tmp, "한겨레.csv")

# 연관분석을 위한 파일 저장
write.table(한겨례$기사, file = "한겨례.txt", )

par(mfrow = c(3, 3))

tr <- read.transactions("한겨례.txt")
image(tr)
str(tr)
tr@data@Dim
tr@itemInfo

rules <- apriori(tr, parameter = list(supp = 0.01))
plot(rules)

install.packages("treemap")
library(treemap)
jo <- c(1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3)
name <- c(
  "박이정", "오현승", "조우현", "심현수",
  "최규형", "김태현", "이한결",
  "김현진", "신우진", "박인영", "이의진"
)
df <- data.frame(jo, name)
df

par(mfrow = c(1, 1)) # 1행,1열
treegraph(df, index = c("jo", "name"), show.labels = TRUE)
treemap(df, index = c("jo", "name"), vSize = "jo", show.labels = TRUE)
