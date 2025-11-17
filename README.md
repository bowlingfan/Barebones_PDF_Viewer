# Custom PDF Viewer
Barebones PDF Viewer that attempts to simplify the User Interface of viewing a PDF. Includes the most basic features such as zooming, rotating, and opening a new pdf. Page turning is supported with keyboard (through pressing the left/right arrow keys or the A, D keys). This also supports zooming in and zooming out with CTRL + Scroll wheel. This also supports opening new PDFs directly from File Explorer.

This was created with PyQT (for User Interfaces) and PyMuPDF (for reading the PDF).

## Notes
There is a current bug if you attempt to "Open With" this program for the first time (_It is recommended to checkmark the box stating to "always open .PDF files with this program"_), which it will throw an error stating that a text file's permission for access is denied. I am not sure on how to fix this bug, but the program should still run fine if you just open the pdf file itself (double clicking it).
<p align="center">
  <img width="378" height="333" alt="unexpected" src="https://github.com/user-attachments/assets/654f7853-5f57-42c8-9ebc-555e58f6c7fe" />
</p>

## Credits
* [QT](https://www.qt.io/), a package meant for creating User Interfaces.
* [PyMuPDF](https://mupdf.com/pymupdf), a package allowing the ability to read PDFs.

<img width="400" height="781" alt="view1" src="https://github.com/user-attachments/assets/c328f7c5-5edc-47e3-ac7c-2b00fd3f9a86" />
<img width="400" height="775" alt="view2" src="https://github.com/user-attachments/assets/255163ef-72cb-4acb-b978-b0825bd67de5" />


