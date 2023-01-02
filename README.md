# sd_gimai
Game Talk Scenes Builder

- イラストと音声をあわせた作品をつくるためのツールです。
- 義妹です。

# 前提

- MaiNovelをエンジン部のみ内蔵しています
  - https://github.com/Zuntan03/MaiNovel
- JSONファイルの手編集をしなくても作品が作れます
  - VSCodeのインストールは必要ありません
- 音声編集ははCOEIROINKを利用する想定です
  - https://coeiroink.com/
  - CPU版でもGPU版でもお好きなほうを
  - CUDAの競合による環境破壊に関して私は一切の責任を負いません
- ゲームは作れません
  - 選択肢や条件分岐など最低限のゲーム性の実装もないので
  - そもそもゲーム性が必要かどうかというのが悩みどころ

# 制作の流れ

- COEIROINKにセリフを打ち込んでいきます。
  - sd_gimaiではセリフ以外の文字表現は一切できません。
- 「音声書き出し」をすると 001 から始まる wav ファイルが保存されます。
  - ファイル名は数字3桁で始まっていればそのままの名前で大丈夫です。
- セリフが書けたら「テキストを繋げて書き出し」をして、名前を s000.txt にしてwavと同じ場所に保存します。
- 1111で画像を生成したら s000mXXX.png という名前で保存します。XXXはwavファイル名と同じ数字です。
  - 画像は不足していても動作しますが、最初の 001 は必須です。
  - 音声は省略できないようです。(mainovelの制約?)
- シーンを切り替えたい場合、セリフが1000以上になる時は s001.txt を作って同様に作業します。
  - 画像ファイル名も s001m001.png からになります。
- できたファイルを extensions/sd_gimai/project の下に移動します。
  - サブディレクトリも見に行きます。
- sd_gimai の List で Reload すると、voiceとimageの存在確認ができます。
  - ボタンを押すとPreviewタブの中で再生確認ができます。
- mainovelのjsonを細かくいじりたい場合は project/mainovel.json を作ります。(後述)
- Buildタブでゲームを出力できます。
- server.bat でローカルでも動作確認ができます。

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

- project以下には1つの作品しか設置できません。
  - imageファイル名はuniqueになるはずです。
  - voiceの先頭3桁が同じファイルも存在しない想定です。
- 最初にダミーのm000が追加されます
  - MaiNovelではm000必須だがCOEIROINKのwavが001から始まっているため
  - imageは001のコピーから000を作ります
  - voiceは無音のファイルを自動的に設置します

# 今後の展望

- 需要があるんなら音声部とエンジン部の複数対応
  - MoeGoe?
  - ティラノスクリプト?

# 望み

- できれば無償の公開作品に使われることに期待します
- 営利目的での利用後はオープンソースコミュニティへの還元を
