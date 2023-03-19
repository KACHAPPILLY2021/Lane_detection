<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">


  <h1 align="center">Lane Detection and Turn Prediction </h1>


</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary><h3>Table of Contents</h3></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#demo">Demo</a></li>
      </ul>
    </li>
    <li>
      <a href="#pipeline">Pipeline</a>
      <ul>
        <li><a href="#straight-lane-detection">Straight Lane Detection</a></li>
        <li><a href="#turn-prediction">Turn Prediction</a></li>
        <li><a href="#report">Report</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#usage">Usage</a></li>
      </ul>
    </li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project



This repository contains code to detect lanes on straight and curved roads using classical approach of computer vision to mimic ```Lane Departure Warning System``` in self-driving cars. Concepts of **homography**, **polynomial curve fitting**, **hough lines**, **warping,** and **unwarping** have been implemented to get the results. The program also predicts turn on curved roads by computing the radius of curvature.
Two additional programs were implemented for Histogram Equalization and Adaptive Histogram Equalization, which would be discussed in great detail in Report.

The detailed problem statement can be found here. [Problem_Statement](https://github.com/KACHAPPILLY2021/Lane_detection/blob/main/problem_statement.pdf)


<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Demo

<div align="center">

<!-- Input | Histogram Equalization | Adaptive Histogram
--- | :---: | --- | 
![input](https://user-images.githubusercontent.com/90359587/226152684-48412f88-fae2-4f0c-8dfb-9a4dcd133674.gif) | ![out1](https://user-images.githubusercontent.com/90359587/226152698-a55f37d4-4974-406d-8961-6ed2a73a7e9f.gif) | ![adapt](https://user-images.githubusercontent.com/90359587/226152712-b61bd842-6ed1-44fc-81e2-e7936aea68a2.gif) -->

Input Data | 
:---: | 
![input](https://user-images.githubusercontent.com/90359587/226152684-48412f88-fae2-4f0c-8dfb-9a4dcd133674.gif) |
Histogram Equalization | 
![out1](https://user-images.githubusercontent.com/90359587/226152698-a55f37d4-4974-406d-8961-6ed2a73a7e9f.gif) |
Adaptive Histogram | 
![adapt](https://user-images.githubusercontent.com/90359587/226152712-b61bd842-6ed1-44fc-81e2-e7936aea68a2.gif) |
	
</div>

<div align="center">


  <h3 align="center"> Lane Detection</h3>


</div>

![p2-solution-2-online-video-cutte](https://user-images.githubusercontent.com/90359587/224575694-089634a3-34dc-4580-b4e6-639e54730c8c.gif)

[![Youtube](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtu.be/ALf60N8Jc4w)

<div align="center">


  <h3 align="center"> Turn Prediction</h3>


</div>

https://user-images.githubusercontent.com/90359587/224575766-424a6eb2-0077-4ffa-bf47-9042d5dce52e.mp4

[![Youtube](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtu.be/swtyh6bpl-I%09)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Pipeline and Reports -->
## Pipeline

The pipelines are represented as block diagrams and their explanation is as follows:

### Straight Lane Detection

<img src="https://github.com/KACHAPPILLY2021/Lane_detection/blob/main/pipe_img/pipe1.JPG?raw=true" alt="straight lane">

1) Read and converted frame into grayscale.
2) Performed blurring operation to filter out cars and unwanted lanes.
3) Parameter tuned CannyEdge to detect atleast the main lanes.
4) Detected all the straight lines by using HoughlinesP, the parameters are finely tuned.
5) Using the first line output from Hough as solid, the dashed lanes were determined 
using the following approach: 
    - The slope direction of the solid lane was calculated (+ve or -ve).
    - Using this, the equation of the line for the given slope was calculated and plotted green.
    - Dashed lines were selected whith slopes that had opposite signs from solid lane.

### Turn Prediction
<p align="center">
<img src="https://github.com/KACHAPPILLY2021/Lane_detection/blob/main/pipe_img/pipe2.JPG?raw=true" height="500" alt="turn lane">
	
1) Inbuilt opencv function used to get top-view of required section.
2) GaussianBlur to remove noise from image.
3) Yellow lanes detected, by converting in ‘hsv' color format and applying mask.
4) The detected yellow pixels are passed into ‘np.polyift’ to get curve equation.
5) Top-view image converted into grayscale.
6) White lanes detected, applying threshold.
7) The detected white pixels are passed into ‘np.polyift’ to get curve equation. 
8) Both the detected lanes are merged into a single image.
9) The top-view is converted back into original view.
10) The final image is generated by concatenating different images.
	
* Computed the radius of curvature using [curve equation](https://www.cuemath.com/radius-of-curvature-formula/).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Report

Detailed decription for this project can be found in this [Report](https://github.com/KACHAPPILLY2021/Lane_detection/blob/main/p2_report.pdf).
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->

## Getting Started

These are the instructions to get started on the project.
To get a local copy up and running follow these simple steps.

### Prerequisites
* Python 3.6 or above
* Libraries - OpenCV, Numpy
* OS - Linux (tested)


### Usage

1. Clone the repo
   ```sh
   git clone https://github.com/KACHAPPILLY2021/Lane_detection.git
   ```
2. Open the folder ```Lane_detection``` in IDE and RUN each file or navigate using terminal
   ```sh
   cd ∼ /Lane_detection
   ```
3. To run Histogram equalization (Appx. 20s to finish displaying output):
   ```sh
   python3 solution_1a.py
   ```
4. To run Adaptive Histogram equalization:
   ```sh
   python3 solution_1b.py
   ```
6. To run solid and dashed lane classification:
   ```sh
   python3 solution_2.py
   ```
7. To run Turn Prediction program:
   ```sh
   python3 solution_3.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Jeffin Johny K - [![MAIL](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:jeffinjk@umd.edu)
	
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://github.com/KACHAPPILLY2021)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](http://www.linkedin.com/in/jeffin-johny-kachappilly-0a8597136)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See [MIT](https://choosealicense.com/licenses/mit/) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
