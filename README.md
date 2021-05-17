# SetAI
Simple bot to play on the website SetWithFriends

Uses a TensorFlow Keras based Image Classifier to turn the screenshots of the cards into a Card object so the solver can find a set and click it

Needs:
 - PIL (used to get screenshots)
 - tensorflow
 - numpy
 - win32api, win32con (for mouse controls therefore currently only works on windows)
