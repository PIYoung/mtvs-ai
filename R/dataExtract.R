install.packages("dplyr")
install.packages("ggplot2")

library("ggplot2")
library("dplyr")
library("psych")

kbo <- read.csv("jupyters/csvs/k.csv", sep = "\t")
head(kbo, 10)
str(kbo)
summary(kbo)

boxplot(scale(kbo[, 3:21]))
plot(kbo)

pairs.panels(kbo[3:20])

# 데이터를 정렬할 때 쓰는 함수는 arrange()
head(arrange(kbo, 팀))
head(arrange(kbo, desc(팀)))
tail(arrange(kbo, desc(팀)), 5)

# 지금 보기는 식이 간단하지만 명령어가 길어지면 이렇게 함수(함수(함수(함수())))로 점점 모양이 복잡해집니다.
# 그래서 dplyr는 '파이프(pipe)'라는 기능을 가지고 있습니다.
# R에서 파이프는 '%>%'로 표시합니다.
# 파이프를 쓰면 바로 위에서 쓴 명령어를 arrange(kbo, desc(팀)) %>% tail(5)로 바꿀 수 있습니다.
arrange(kbo, desc(팀)) %>% tail(5)

# 행을 추출할 때는 filter()
# 열을 추출할 때는 select()
filter(kbo, 연도 == 2017) %>% head()
select(kbo, 안타, X2루타, X3루타, 홈런)
filter(kbo, 연도 == 2017) %>%
  select(안타, X2루타, X3루타, 홈런) %>%
  head()
filter(kbo, 연도 == 2017) %>%
  select(-안타, -X2루타, -X3루타, -홈런) %>%
  head()

# 새로 열을 만들어 넣어야 하는 할 때 쓰는 함수는 mutate()
kbo %>%
  mutate(타율 = 안타 / 타수) %>%
  head()

# 그루핑(grouping) 그리고 tibble
# tibble은 데이터 프레임을 현대적으로 업그레이드한 형태
kbo %>% group_by(연도)
kbo %>%
  group_by(연도) %>%
  summarise(타율 = sum(안타) / sum(타수))
#  꼭 mutate()를 쓰시고 싶거나 총 안타와 총 타수를 표시하고 싶으실 때
kbo %>%
  group_by(연도) %>%
  summarise(총안타 = sum(안타), 총타수 = sum(타수)) %>%
  mutate(타율 = 총안타 / 총타수) # nolint

# 2001년 리그 평균 타율
kbo %>%
  group_by(연도) %>%
  summarise(타율 = sum(안타) / sum(타수)) %>%
  filter(연도 == 2001) # nolint
# 리그 평균 타율이 제일 높았던 연도
kbo %>%
  group_by(연도) %>%
  summarise(타율 = sum(안타) / sum(타수)) %>%
  filter(타율 == max(타율)) # nolint
kbo %>%
  group_by(연도) %>%
  summarise(타율 = sum(안타) / sum(타수)) %>%
  filter(타율 == max(타율))

avg <- kbo %>%
  group_by(연도) %>%
  summarise(타율 = sum(안타) / sum(타수))

kbo %>%
  group_by(연도) %>%
  summarise(타율 = sum(안타) / sum(타수)) -> avg2 # nolint

ggplot(data = avg, aes(x = 연도, y = 타율)) +
  geom_line()
kbo %>%
  group_by(연도) %>%
  summarise(타율 = sum(안타) / sum(타수)) %>%
  ggplot(., aes(x = 연도, y = 타율)) +
  geom_line()



kbo <- mutate(kbo,
  타율 = 안타 / 타수,
  출루율 = (안타 + 볼넷 + 몸에.맞는.공) / (타수 + 볼넷 + 몸에.맞는.공 + 희생플라이),
  장타력 = 총루타 / 타수,
  ops = 출루율 + 장타력
)
str(kbo)

kbo %>% filter(ops >= 0.7 & 홈런 < 70)

kbo %>%
  filter(ops >= 0.7 & 홈런 < 70) %>%
  summarise(n())

kbo %>%
  filter(ops < 0.7 | 홈런 >= 70) %>%
  summarise(n())

kbo %>%
  filter(ops >= 0.7 & 홈런 < 70 & 연도 %in% 1982:1990)

kbo %>%
  filter(ops >= 0.7 & 홈런 < 70 & 연도 %in% 1982:1990) %>%
  select(연도, 팀, 경기, 득점, 도루, 도루실패) %>%
  mutate(평균득점 = 득점 / 경기, 도루성공률 = 도루 / (도루 + 도루실패))

kbo %>%
  mutate(그룹 = ifelse(연도 <= 1990, "A",
    ifelse(연도 <= 2000, "B",
      ifelse(연도 <= 2010, "C", "D")
    )
  )) %>%
  group_by(그룹) %>%
  summarise(평균희생번트 = mean(희생번트))

kbo %>%
  group_by(팀) %>%
  summarise(병살 = sum(병살)) %>%
  arrange(desc(병살)) %>%
  head(3)
