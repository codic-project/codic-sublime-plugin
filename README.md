# Codic Sublime Text Plugin
Sublime text から [codic](https://codic.jp/) の機能を呼び出すプラグインです。

![codic plugin](./screenshot.png)

## インストール
いまの所Package Contorlには対応していません。以下の手順で、Githubからインストールしてください。

1. コマンドパレット <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> →  "Package Control: Add Repository" を選択し、以下のURLを追加。
 
 `https://github.com/codic-project/codic-sublime-plugin`

2. コマンドパレット <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> →  "Package Control: Install Package" を選択し、「codic-sublime-plugin」を選択し、インストール。

3. コマンドパレット <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> → "Codic: Set Access Token" でAccess tokenを設定。Access tokenは、[codic](https://codic.jp/)にサインアップ後、APIステータスのページより取得できます。

## 使い方
コマンドパレット → "Codic: Generate Naming" <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>D</kbd> で入力パネルが表示されるので、日本語を入力するとネーミングが生成されます。またテキストを選択して、Ctrl+Shift+Dでも実行できます。Macは入力パネルで日本語が入力できないバグがあるので、基本こっちですね。

## その他コマンド
- プロジェクトの変更 - コマンドパレット → "Codic: Select Project"
- 生成されるネーミングのケースの変更 - コマンドパレット →  "Codic: Select Letter Case"

## その他
codicのプラグインは、他にも以下があります。基本的には同じAPIを使っているので機能に違いはありせんので、
使い易いヤツを選んだらいいと思います。

- <https://github.com/naoyukik/SublimeCodic> - 高機能
- <https://github.com/airtoxin/codic-sublime> - Package Controlに対応

## TODO
- Supports Multi-selection / Multiline selection.
- airtoxin さんのプラグインに合流w
