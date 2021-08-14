<h1 class="code-line" data-line-start=0 data-line-end=1 ><a id="Intruduction_0"></a>Intruduction</h1>
<p class="has-line-data" data-line-start="2" data-line-end="3">Direct volume rendering is effective way to visualize threedimensional scalar field. In contrast to indirect volume rendering, which maps certain parts of volume data to points, lanes or surfaces, direct volume rendering map volume data directly to optical properties, such as color and transparency. Assigning optical properties to the voxel data is done by a transfer function.</p>
<p class="has-line-data" data-line-start="4" data-line-end="5">Transfer function is part of the traditional visualization pipeline: data acquisition, processing, visual mapping and rendering and are crucial for revealing the relevant features present in data studied. For example, in medical visualization, it can help user distinguish different regions by setting different colors and opacity to the same material, such as bone, soft tissue and vessel.</p>
<p class="has-line-data" data-line-start="6" data-line-end="7">However, a good transfer function is difficult to generate. This motivated many studies on transfer function design, which focused on development of new high-level user interfaces for transfer function design and new methods for automatic generation of transfer function. This seminar proposes new approach - exploratory tool that eases a process of creating and adjusting transfer functions. Tool allows user browsing through variations of the currently applied transfer function. Transfer function recommendations are presented to the user in the form of small low-resolution previews, in similar fashion to design galleries:</p>
<p class="has-line-data" data-line-start="9" data-line-end="10">
  
 
 ![alt text](https://github.com/gobica/transfer-function-design-gallery/blob/main/gallery-first-iteration.PNG "Design gallery1"  | width=300)

<h2 class="code-line" data-line-start=11 data-line-end=12 ><a id="Prerequisites_11"></a>Prerequisites</h2>
<ul>
<li class="has-line-data" data-line-start="12" data-line-end="13">Python 3.7</li>
<li class="has-line-data" data-line-start="13" data-line-end="14">Anaconda enviornment</li>
<li class="has-line-data" data-line-start="14" data-line-end="16">VTK 8.2.0</li>
</ul>
<h2 class="code-line" data-line-start=16 data-line-end=17 ><a id="How_to_run_16"></a>How to run</h2>
<p class="has-line-data" data-line-start="17" data-line-end="18">run <a href="http://main.py">main.py</a> script with <code>python main.py</code></p>
<p class="has-line-data" data-line-start="19" data-line-end="20">
 
  
   ![alt text](https://github.com/gobica/transfer-function-design-gallery/blob/main/rendered.PNG "Rendered model"  | width=300)

