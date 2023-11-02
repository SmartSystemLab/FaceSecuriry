# FaceSecuriry
- A attendance system based on facial recognition.

- This repository contains code that uses the power of artificial intellegence to mark people's attendance when a camra recognises their face.

- the libaies used in this projct are:
- * FaceRec
  * Open Cv
  * Pandas
  * Flask

## How the project runs
### FACE REC
- A dataset containing faces was fed into the The state of the art face Recognition library
- This library generates face encodings that can uniquely and corrctly identify a person's face
- the libary also contains a face comparison feature that helps you to compare faces (encodings),
- * so if the faces are the same person it returns TRUE and FALSE if th yare not the same person.
 
### PANDAS
- once a face has been detected, a label is placed on the face and displayed.
- the exact time of recognition of the face is ecorded ans stored

### FLASK
- The software was deployed through a flask wb interface ( deploy.py)

