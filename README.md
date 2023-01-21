# sd_gimai
Game Talk Scenes Builder

- イラストとセリフと音声をあわせた作品をつくるためのツールです。

# サンプル

- https://aka7774.netlify.app/
- 義妹です。

# 前提

- イラスト、音声、セリフはそれぞれのソフトで作成する必要があります
- MaiNovelをエンジン部のみ内蔵しています
  - https://github.com/Zuntan03/MaiNovel

## 音声ファイル作成

以下のソフトウェアが便利です(自己責任)

- VOICEVOX
  - https://voicevox.hiroshiba.jp/
  - 中品質(自称)
- COEIROINK
  - https://coeiroink.com/
  - VOICEVOXより高品質に感じる
- MoeGoe
  - https://github.com/CjangCjengh/MoeGoe
  - https://huggingface.co/spaces/skytnt/moe-tts
  - モデルデータが豊富
  - 商用利用不可
  - UIが使いにくく調教しづらい
  - 中国語訛りになりがち

# 制作の流れ

## 音声の保存

### VOICEVOX/COEIROINKを使う場合 

- VOICEVOX/COEIROINKにセリフを打ち込んでいきます。
  - 内部構造は違いますが画面の見た目はほぼ一緒です。
- 「音声書き出し」をすると 001 から始まる wav ファイルが保存されます。
  - ファイル名は数字3桁で始まっていればそのままの名前で大丈夫です。
- セリフが書けたら「テキストを繋げて書き出し」をして、名前を s000.txt にしてwavと同じ場所に保存します。

### VOICEVOX/COEIROINK以外を使う場合

- テキストエディタにセリフを打ち込んでいきます。
  - Notepad++など行番号が出るやつがおすすめです。
- name(後述)とセリフをカンマ区切りで一行にします。
  - 一括編集には LibreOffice Calc などが便利かもしれません。
- このファイルを s000.txt という名前で保存します。

### VSCode(MaiNovel)を使う場合

- build後にMaiNovelを使って音声ファイルを出力します(他とは手順が逆になります)
- nameは空白で構いません(カンマは必要です)

### MoeGoe GUIを使う場合

- XXX行目のセリフに対応する音声を s000mXXX.wav という名前で保存します。
- MoeGoe(CLI)をsd_gimaiから使わないのであればnameは空白で構いません(カンマは必要です)

### MoeGoe(CLI)を使う場合

- MoeGoe は Windows 用のバイナリをダウンロードしてください。
  - Windows以外では(PyOpenJTalkが入るので) MoeGoe.py から実行できるかも知れません。
- セリフが書けたら sd_gimai の「MoeGoe Actors」タブから使いたい声の name を取得します。
  - moe-tts をダウンロードして saved_model を指定し Reload ボタンを押します
  - 「0:0:綾地寧々」のように、数字とコロンが入るようにコピーしてください

```
0:0:綾地寧々,こんにちは。
0:0:綾地寧々,私はバナナが大好きです。
```

- lang に Japanese が含まれるものが日本語対応です
- 声を選ぶために、IDとサンプルメッセージを指定して「MoeGoe Generate Sample」を押せば、すべてのActorsのwavが生成されます。
  - IDはコロンの一番左の数字です。

- sd_gimai の「Project Viewer」タブで「Reload」すると内容を画面に表示できます。
- 「Generate MoeGoe All」を押します。
  - あるいは voice ボタンで1行だけ出力して確認できます。

### 長編作品の場合

- シーンを切り替えたい場合、セリフが1000以上になる時は s001.txt を作って同様に作業します。
  - 画像ファイル名も s001m001.png からになります。

## 画像の保存

- 1111で画像を生成したら s000mXXX.png という名前で保存します。
  - XXXはwavファイル名と同じ数字です。
  - 画像は不足していても動作しますが、最初の 001 は必須です。

## ファイルの設置

- できたファイルを extensions/sd_gimai/project の下に移動します。
  - サブディレクトリも見に行きます。
- sd_gimai の「Project Viewer」で Reload すると、voiceとimageの存在確認ができます。
  - imageボタンを押すと「Preview Image」タブで表示確認ができます。
- 必要に応じて画像と音声の形式を変換します。

## 画像形式の変換

- ファイルサイズ(通信容量)削減に期待できます

### sd_infotextsを使う場合

- https://github.com/aka7774/sd_infotexts
- 画像生成の設定はInfotext Exの推奨に従います。
  - https://github.com/aka7774/sd_infotext_ex
- 画像を出力したら extensions/sd_infotexts/png フォルダに保存します。
  - 画像を変更したい時は「PNG to TXT」「Copy TXT」を実行し edit_txt の中身を書き換えます。
  - Script から画像の一括生成が出来ます。
- webp への一括変換(拡大、文字入れ)が出来ます。

## 音声形式の変換

- ファイルサイズ(通信容量)削減とブラウザ互換性に期待できます

### ffmpegを使う場合

- https://ffmpeg.org/
  - バイナリをダウンロードしてください。一応full推奨。
- List タブの Path to ffmpeg.exe を入力します
- 「Generate mp4 aac All」を押します
  - 指定した拡張子の音声がすべて拡張子mp4のaacコーデックに変換されます
  - 内蔵の aac ライブラリを使用します
    - libfdk_aacはLICENSEの都合でバイナリ配布できないので対応しません

## ビルド

- 変換後の拡張子を再設定して Reload ボタンを押し、ファイルの確認をします。
- mainovelのjsonを細かくいじりたい場合は project/mainovel.json を作ります。(後述)
- 「Build」ボタンでゲームを出力できます。
- server.bat でローカルでも動作確認ができます。

### project/mainovel.json

Buildされるjsonに合体されます。

```
{
	"config": {
		"title": "hogehoge",
		"audioInterval": 1000,
		"credit": "aka7774"
	}
}
```

以下の値は固定です。

```
    "sceneCodeFormat": "000",
    "messageCodeFormat": "000",
```

以下の値はUIからの入力で上書きされます。

```
    "imageFormat": "png",
    "audioFormat": "wav"
```

## 公開

- デフォルトでR18指定になっています。
  - 不要であれば index.html を編集して外してください。
- server.bat は削除してかまいません。
- アダルト可でファイルを設置できる無料レンタルサーバーは貴重です。
  - FC2はKYCが強化されて身分証明書と契約書のアップロードが必要になっていた
  - Wixはファイルがアップロードできない

# 制限事項

- ゲームは作れません
  - 選択肢や条件分岐など最低限のゲーム性の実装もないので
  - そもそもゲーム性が必要かどうかというのが悩みどころ
- ボイスつきのセリフ以外の文字表現は一切できません
  - ボイスと表示を変えるには、wavを設置してからtxtを書き換える手があります
- 音声ファイルは省略できないようです
- project以下には1つの作品しか設置できません。
  - imageファイル名はuniqueになるはずです。
  - voiceの先頭3桁が同じファイルも存在しない想定です。
- 最初にダミーのm000が追加されます
  - MaiNovelではm000必須だがVOICEVOX/COEIROINKのwavが001から始まっているため
  - imageは001のコピーから000を作ります
  - voiceは無音のファイルを自動的に設置します
- MoeGoeは恐らく3.0.1でしか動きません
  - コマンドラインの対話を決め打ちしているので内容が狂うと話が噛み合わなくなります
  - 対話の無い安定したバイナリがあれば移行してもいいけど恐らく枯れたと判断
- VITSモデルの読み込みには info.json への記述が必要です

# 今後の展望

- Linux対応(readmeに追記する程度を想定)
- 需要があるんならエンジン部の複数対応
  - ティラノスクリプト

# 望み

- できれば無償の公開作品に使われることに期待します
- 営利目的での利用後はオープンソースコミュニティへの還元を
