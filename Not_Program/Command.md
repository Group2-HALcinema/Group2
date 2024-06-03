# よく使うGitコマンド

## Gitの初期設定を行う
```bash
git config --global user.name "XXXX"
git config --global user.email "XXXX@hogehoge.com"
```

## リモートから作業環境をクローンする
```bash
git clone https://github.com/XXXX/XXXXX.git
```

## ローカルにリポジトリを作成し、リモートにプッシュする
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/XXXX/XXXXX.git
git push -u origin master
```

## リモートから変更を取得する
```bash
git pull origin <ブランチ名>
```

## ファイルの登録
```bash
git add <ファイル名>
```

## ファイルの変更や追加のコミット
```bash
git commit -m "コミットメッセージ"
```

## ローカルの変更を確認
```bash
git status
```

## commitの変更履歴を見る
```bash
git log
```

## リモートにプッシュ
```bash
git push origin <ブランチ名>
```

## addの取り消し
```bash
git reset HEAD <ファイル名>
```

## commitの取り消し
```bash
git reset --hard HEAD^
```
--hard：コミットを消した上でワークディレクトリの内容も書き換えたい場合

--soft：ワークディレクトリの内容はそのままでコミットだけを取り消したい場合

HEAD^：直前のコミット

HEAD~(n)：n個前のコミット

## ローカルでブランチを作成
```bash
git branch <ブランチ名>
```

## ローカルでブランチの切り替え
```bash
git checkout <ブランチ名>
```

## ブランチの削除
```bash
git branch -d <ブランチ名>
```

## プルリクの内容をマージ前にローカル環境で稼働確認する
```bash
git fetch origin pull/<プルリクのID>/head:<任意の名前>
```
ローカル上にプルリクされたブランチが作成される

<任意の名前>はPR-<プルリクのID>とかにするといい