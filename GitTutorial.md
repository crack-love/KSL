깃 듀토리얼
=============
참조 1. 원숭이도 이해할 수 있는 Git : https://backlog.com/git-tutorial/kr
참조 2. "Git pro2" e-book : https://git-scm.com/book/ko/v2
##1.기본
$ git status : 현재 상태 확인
$ git add <file> : 파일을 스테이징에 추가한다
$ git commit : 스테이징 파일들 현재 상태 저장
HEAD : 포인터로 현재 커밋을 가리키고 있다
~ : 접미사로 그 이전을 뜻할 수 있다 (HEAD~~~, HEAD~4 : HEAD 3번 전)
인자로서 <commit>과 <branch> :commit이 들어와야 할 자리에 branch가 들어와도 작동한다.

##2.로그
$ git log : 이력 확인
$ git log -3 : 최근 3개 이력 확인
$ git log --graph --oneline : 그래프로 확인 (한 줄)
$ git log --decorate : 태그 정보를 포함한 이력 확인 

##3.브랜치
$ git branch : 브랜치 조회, 현재 브랜치(HEAD)는 *로 표시돼있다
$ git branch -d <branchname> : 브랜치 삭제
$ git checkout <branch> : HEAD를 브랜치로 이동
$ git checkout -b <branch> : 브랜치 생성, 이동
$ git merge <commit> : HEAD에 commit(branch) merge
$ git rebase <commit> : 현재를 대상 commit(branch) 뒤에 concat 시켜버린다, 이후 대상 브랜치서 merge 수행필요
$ git rebase --continue : (conflit된 파일 수정한 뒤) rebase 계속 시도
$ git rebase --abort : rebase 자체 취소

##3.원격저장소
$ git pull : 원격 저장소의 데이터를 로컬 저장소에 가져와 병합하기 (fetch + merge)
$ git fetch : 원격 저장소의 데이터를 로컬에 가져오기만 하기, 이 때 가져온 최신 커밋 이력은 이름 없는 브랜치로 로컬에 가져오게 됩니다. 이 브랜치는 'FETCH_HEAD'의 이름으로 체크아웃 할 수도 있습니다.
$ git push : 로컬 저장소의 데이터를 원격 저장소로 밀어넣기. (주의) 원격 저장소에서 모두가 공유하고 있는 커밋은 기본적으로 덮어쓰거나(overwrite) 임의로 변경해서는 안됩니다.

##3.태그
$ git tag : 태그 목록
$ git tag -n : 태그 목록(주석 포함)
$ git tag <tagname> : HEAD에 태그 설정
$ git tag -a <tagname> : 주석 달린 태그 설정
$ git tag -am "주석" <tagname> : 주석 달린 태그 설정(즉시)
$ git tag -d <tagname> : 태그 삭제

##3.고급(커밋수정)
$ git commit --amend : 직전 커밋 수정누락된 파일을 새로 추가하거나 기존의 파일을 업데이트 해야할 때이전 커밋의 설명을 변경하고 싶을 때
$ git revert <commit> : 대상 커밋을 지우는 커밋을 함(지우는 커밋이 로그에 새로 추가됨)
$ git reset --hard <commit> : 돌아가기. commit/merge도 취소. 지우는 커밋이 추가되지 않고 완전히 클린하게 지워버리며 이전으로 돌아감. HEAD~~ HEAD~ 등 이용reset 전의 커밋은 'ORIG_HEAD'라는 이름으로 참조할 수 있음. 실수로 reset 을 한 경우에는, 'ORIG_HEAD'로 reset
$ git cherry-pick <commit> : 다른 브랜치의 커밋을 쏙 빼서 가져옴
$ git rebase -i <commit> : 현재를 대상 커밋 뒤로 이동시키고 사이에 있는 커밋을 어떻게 처리할 것인지 정함 (pick, squash, ...) 커밋에 squash를 이용하면 커밋을 (직전과)통합시키는 결과. 따라서 맨 처음은 squash를 이용할 수 없다.예제_커밋머지)pick 5265210 커밋설명1squash d25e56b 커밋설명2squash e93b7d8 커밋설명3예제_커밋수정)edit 5265210 커밋설명1이후 git 에서 시키는데로 수정을 수행하면 된다.
$ git merge --squash <commit(branch)> : 대상 branch상의 모든 commit을 하나로 병합한 후 현재 branch에 추가한다.