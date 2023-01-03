# sd_gimai
Game Talk Scenes Builder

- イラストとセリフと音声をあわせた作品をつくるためのツールです。

# サンプル

- https://aka7774.netlify.app/
- 義妹です。

# 前提

- イラスト、音声、セリフはそれぞれのソフトで作成する必要があります
  - VSCodeのインストールやJSONファイルの手編集は必須でなくなります
- MaiNovelをエンジン部のみ内蔵しています
  - https://github.com/Zuntan03/MaiNovel
  - build後のmainovel.jsonを利用することでMaiNovel本来の使い方も出来るはず
- 音声はCOEIROINKかMoeGoeが便利です(自己責任)
  - https://coeiroink.com/
  - https://github.com/CjangCjengh/MoeGoe
  - https://huggingface.co/spaces/skytnt/moe-tts

# 制作の流れ

## COEIROINKを使う場合 

- COEIROINKにセリフを打ち込んでいきます。
- 「音声書き出し」をすると 001 から始まる wav ファイルが保存されます。
  - ファイル名は数字3桁で始まっていればそのままの名前で大丈夫です。
- セリフが書けたら「テキストを繋げて書き出し」をして、名前を s000.txt にしてwavと同じ場所に保存します。

## MoeGoeを使う場合

- MoeGoe は Windows 用のバイナリをダウンロードしてください。
  - MoeGoe GUIは不要です。
  - Windows以外では(PyOpenJTalkが入るので) MoeGoe.py から実行できるかも知れません。
- テキストエディタにセリフを打ち込んでいきます。
  - Notepad++など行番号が出るやつがおすすめです。
- セリフが書けたら sd_gimai の MoeGoe タブから使いたい声の name を取得します。
  - moe-tts をダウンロードして saved_model を指定します
  - 「0:0:綾地寧々」のように、数字とコロンが入るようにコピーしてください
- name とセリフをカンマ区切りで一行にします。
  - 一括編集には LibreOffice Calc などが便利かもしれません。

```
0:0:綾地寧々,こんにちは。
0:0:綾地寧々,私はバナナが大好きです。
```

- このファイルを s000.txt という名前で保存します。
- sd_gimai の List タブで「Reload」すると内容を画面に表示できます。
- 「Generate MoeGoe All」を押します。
  - あるいは voice ボタンで1行だけ出力して Preview タブで確認できます。

## 画像の配置(共通)

- 1111で画像を生成したら s000mXXX.png という名前で保存します。
  - XXXはwavファイル名と同じ数字です。
  - 画像は不足していても動作しますが、最初の 001 は必須です。

## [Optional] sd_infotextsを使う画像生成

- https://github.com/aka7774/sd_infotexts
- 画像生成の設定はInfotext Exの推奨に従います。
  - https://github.com/aka7774/sd_infotext_ex
- 画像を出力したら extensions/sd_infotexts/png フォルダに保存します。
- 画像を変更したい時は「PNG to TXT」「Copy TXT」を実行し edit_txt の中身を書き換えます。
- Script から画像の一括生成が出来ます。
- webp への一括変換(拡大、文字入れ)も出来ます。

## ビルド(共通)

- できたファイルを extensions/sd_gimai/project の下に移動します。
  - サブディレクトリも見に行きます。
- sd_gimai の List で Reload すると、voiceとimageの存在確認ができます。
  - ボタンを押すとPreviewタブで再生確認ができます。
- 必要に応じて画像と音声の形式を変換します。
  - 変換後は拡張子を再設定して Reload ボタンを押し、ファイルの確認をします。
- Buildタブでゲームを出力できます。
- server.bat でローカルでも動作確認ができます。

## [Optional] ffmpegを使う音声変換

- https://ffmpeg.org/
- 内蔵の aac ライブラリを使用します
  - libfdk_aacはLICENSEの都合でバイナリ配布できないので対応しません
- ファイルサイズ(通信容量)削減とブラウザ互換性に期待できます

## Tips

- シーンを切り替えたい場合、セリフが1000以上になる時は s001.txt を作って同様に作業します。
  - 画像ファイル名も s001m001.png からになります。
- mainovelのjsonを細かくいじりたい場合は project/mainovel.json を作ります。(後述)

## project/mainovel.json

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

# 制限事項

- ゲームは作れません
  - 選択肢や条件分岐など最低限のゲーム性の実装もないので
  - そもそもゲーム性が必要かどうかというのが悩みどころ
- ボイスつきのセリフ以外の文字表現は一切できません
- 音声ファイルは省略できないようです
- project以下には1つの作品しか設置できません。
  - imageファイル名はuniqueになるはずです。
  - voiceの先頭3桁が同じファイルも存在しない想定です。
- 最初にダミーのm000が追加されます
  - MaiNovelではm000必須だがCOEIROINKのwavが001から始まっているため
  - imageは001のコピーから000を作ります
  - voiceは無音のファイルを自動的に設置します
- MoeGoeは恐らく3.0.1でしか動きません
  - コマンドラインの対話を決め打ちしているので内容が狂うと話が噛み合わなくなります
  - 対話の無い安定したバイナリがあれば移行してもいいけど恐らく枯れたと判断
- VITSモデルの読み込みには info.json への記述が必要です
- MoeGoeに送るテキストの先頭と末尾には自動的に[JA]が付与されます

# 今後の展望

- 入力内容の記憶(config.jsonで出来るけど)
- Linux対応(readmeに追記する程度を想定)
- 需要があるんならエンジン部の複数対応
  - ティラノスクリプト

# 望み

- できれば無償の公開作品に使われることに期待します
- 営利目的での利用後はオープンソースコミュニティへの還元を
