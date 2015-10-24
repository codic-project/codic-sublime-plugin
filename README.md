# Codic sublime text プラグイン
Sublime text から [codic](https://codic.jp/) の機能を呼び出すプラグインです。

## インストール
1. いまの所Package Contorlには対応していません。リポジトリをダウンロードして、Sublime text の Packages ディレクトリの下に配置してください。パッケージディレクトリは、メニュー -> Preference -> Browse  Packages ... から確認できます。
2. インストール後、コマンドパレット (Ctrl+Shift+P) -> 「Codic: Set access token」でAccess tokenを設定します。Access tokenは、[codic](https://codic.jp/)にサインアップ後、APIステータスのページより取得できます。

## 使い方
コマンドパレット -> 「Codic: Generate naming」(Ctrl+Shift+D) で入力パネルが表示されるので、日本語を入力するとネーミングが生成されます。またテキストを選択して、Ctrl+Shift+Dでも実行できます。Macは入力パネルで日本語が入力できないバグがあるので、基本こっちですね。

![codic plugin](https://codic.jp/external/github/sublime.png)

## その他コマンド
- プロジェクトの変更 - コマンドパレット -> 「Codic: Select project」
- ケースの変更 - コマンドパレット -> 「Codic: Chage letter case」

## その他
codicをサポートしているプラグインは、他にも以下があります。同じAPIを使っているので基本的には機能に違いはありせんので、
使い易いヤツを選んだらいいと思います。

- [https://bitbucket.org/dat/sublimecodic](https://bitbucket.org/dat/sublimecodic) - 高機能
- [https://github.com/airtoxin/codic-sublime](https://github.com/airtoxin/codic-sublime) - Package Controlに対応

## TODO
- Supports Multi-selection / Multiline selection.
- airtoxin さんのプラグインに合流w
