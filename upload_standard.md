## Upload Standard

As a task publisher, all you need to do is to upload a zip file, such as `upload.zip`.

### File structure

Here's an example file structure of `upload.zip`. After extract your `.zip` file, we should get and only store the following files.

```
upload                  # The folder
├── meta.json           # Project describer
├── 1.json              # Unlabeled data
├── 2.json
├── 3.json
├── 4.json
├── 5.json
├── 6.json
├── 7.json
├── 8.json
├── 9.json
├── 10.json
└── 11.json
```


### Project describer: `meta.json`

Firstly, you need your `meta.json` to describe your data set.

```json
{
    "projectName": "test",
    "description": "This is a test for se2018.",
    "fault_level": 2
}
```

You can choose 3 values for fault tolerance `fault_level`, which are `0` for turn off, `1` for low level and `2` for high level.

### Unlabeled Data: `1.json`

```json
{
  "projectName": "test",
  "index": 723154,
  "data": "物流速度快，性价比高",

  "task": [
    {
      "mode": "single", 
      "front": "option",
      "aim": "请选择这句话的语言：",
      "label": "中文",
      "choices": ["中文", "英文"]
    },
    {
      "mode": "multiple",
      "front": "box",
      "aim": "请选择这句话的情感：",
      "label": ["开心", "满意"],
      "choices": ["开心", "满意", "失望", "生气"]
    },
    {
      "mode": "open",
      "front": "blank",
      "aim": "请选出句子中的形容词：",
      "label": ["快", "高"]
    }
  ]
}
```

In `1.json`, you need to announce your `projectName`, `index`, `data` and `task`.
- `projectName` is the name of your project.
- `index` is the index of your data. (We recommend to name the json file as index.) 
- `data` is the unlabeled text data.
- `task` includes many subtasks.

In one `task`, you need to announce the `mode`, `front`, `aim`, `label` and `choices` of your subtask.
- `mode` includes `single` for single choice, `multiple` for multiple choice and `open` for whatever you want the users to type in.
- `front` includes `option` for single choice cycles, `box` for multiple choice boxes and `blank` for the boxes whatever you want the users to type in.
- `aim` is the question you want to ask.
- `label` is the answer of `aim`. It can be blank or something you already have and want users to modify if it's not correct.

