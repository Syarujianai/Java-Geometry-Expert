[original repo](https://github.com/yezheng1981/Java-Geometry-Expert)


## Quick Start

- **File Structure**

  - geosolver-master  <font size=2> *parser and visualizer `geosolver`* </font>
    - my_prover.py <font size=2> *Demo* </font>
    - extractor/seg <font size=2> *用于坐标点匹配的字母模板* </font>
  - examples  <font size=2> *`JGEX ` examples* </font>
    - 6_GDD_FULL  <font size=2> *`JGEX ` 提供的测试样例* </font>
    - Rulers  <font size=2>*`JGEX GUI: lemma `*</font>
    - Junior Mathematics  <font size=2>*自己写的测试样例*</font>
  - out <font size=2> *IDEA输出目录* </font>
    - out/artifacts/Java_Geometry_Expert_jar2/Java-Geometry-Expert.jar <font size=2>*打包好的gprover.Main2，供`geosolver my_prover.py`调用*</font>
  - gprover <font size=2>*底层API*</font>
    - Main2.java <font size=2>*`JGEX prover(GDD)`入口*</font>
  - wprover <font size=2>*GUI相关*</font>
    - GExpert.java <font size=2>*`JGEX GUI`入口*</font>

  

- **Enviroment Requirements**

  - `JGEX`: JDK 1.6
  - `geosolver`: 
    - python 2.7
    - 其它见requirements



- **Run Demo**

  - 下载仓库

  - 配置geosolver conda环境

    - `cd geosolver-master`
    - `conda create -n geos python==2.7`
    - `conda install --file requirements.txt`

  - 配置IEDA 并打包`gprover.Main2`及其extend依赖

    - `Import Project`，`Edit Configuration` 中选择主类为`gprover.Main2`，编译并打包成jar: `Build -> Build Artifacts`，`my_prover.py`中修改为`-Djava.class.path`和`-Djava.ext.dirs`分别为输出jar包和相应extend依赖输出路径
    - ps: 若想运行`GUI`，选择主类为`wprover.GExpert`直接`Run`即可 

  - repo内实现了基于模板匹配的字母OCR，为此需要提取字母`A-Z`的所有可能模板并存入`geosolver/diagram/seg/{}`中

    - 如何提取和显示`primitives`参考[Geosolver tutorial](https://github.com/uwnlp/geosolver)

    - 保存字母模板只需修改`geosolver/utils/prep.py`即可 (如下注释部分):

      ```
      /* prep.py */
      count = 0
      def display_image(image, title="", block=True):
          cv2.imshow(title, image)
          // global count
          // count += 1
          // cv2.imwrite("./data/my/{}.png".format(count), image)
          if block:
      		block_display()
      ```

  - 激活conda环境并运行

    - `conda activate geos`

      `NOTE`: 注意`jpype`版本需小于等于`0.6.3`

    - `python my_prover.py`

      `NOTE`: 1. 使用geosolver OCR题目的坐标点，存入`position_{id}.txt`；2. 使用`jpype`调`Java-Geometry-Expert.jar`的`Main2.parse_and_prove_problem(id)`接口，预处理过程中会合并`position_{id}l.txt`和`example_{id}.txt`于`combined_{id}.txt`中然后读取`gterm`最后以返回`String`类型的证明过程



# Tutorial

## **JGEX.gprover** 

- 首先，对测试样例所在的文件夹结构进行说明

  ```
  + Junior Mathematics
  	+ example_{id}.txt  // raw example
  	+ positions_{id}.txt  // geosolver OCR得到的坐标
  	+ combined_{id}.txt  // 合并坐标后的example
  ```

- 其次，测试样例的Formal Language格式如下

  - `EXAMPLE`：题目名

  - `HYPOTHESES`：题目假设 (对应`gib`中的`C_XX`静态变量)

  - `SHOW`：题目结论 (对应`gib`中的`CO_XX`静态变量)

  - `ON_LINE`等均属于尺规作图的command library，具体可参考[gclc_man.pdf](http://poincare.matf.bg.ac.rs/~janicic/gclc/) (chapter3 - GCLC Language)

    ```
    EXAMPLE THM
    HYPOTHESES: 
    POINT A B C D E F
    FOOT D C A B
    ON_LINE E A B
    ON_LINE F C D
    COMPL_ANGLE C A D D F E
    SHOW: PERPENDICULAR A B D E
    ```



### 以GExpert (GUI) 为入口

- gdd证明法于`wprover.PanelProve1.proveGdd`中实现

  ```
  // … 
  gterm gt = condPane.getTerm();  // 从面板中获取gterm
  Prover.set_gterm(gt); // gprover.Prover.set_gterm(g) 
  // … 
  gprover.setProve();  // 设置wprover.GProver.Status为1 
  gprover.start(); // 开启"Prover"线程，绑定wprover.GProver.run() 
  ```

- 调用`wprover.GProver.run()` (`wprover.GProver`为runnable对象)

  ```
  try{  
      if(Status == 0){ 
          // … 
          Prover.run(); // gprover.Prover.fixpoint(gt) 
      }else{
          Boolean t = Prover.prove(); // 返回值: 是否求解成功 
          pprove.displayGDDProve(t); // 调用wprover.PanelProve1类，显示的证明过程 
      }
  }
  ```

- 调用`wprover.PanelProve1`在GUI中显示求解过程 (底层调用以`gprover.Prover.getProveHead()`，结果存储在`Tree： wprover.PanelProve1.top`中)

  

### 以Main2为入口

- 读取对应id的*combined_{id}.txt*并转换为gterm (详见`gprover.gterm`) 然后进行证明，如果坐标文件*positions{id}.txt*存在则进行合并，否则直接读取*example_{id}.txt*

  ```
  parse_and_prove_problem(problem_ids[i], 0);
  ```

  - 初始化可用规则，对应`gib.RValue`布尔变量

    ```
    gib.initRulers();
    ```

  - `Prover.gterm`引用读取的gterm `gt`

    ```
    Prover.set_gterm(gt);
    ```

  - 证明

    ```
    Boolean is_proved = Prover.prove();
    ```

    

    > Prover.prove()

    - 初始化`Prover.db.all_nd`为输入hypothesis  (`nd`{`pred`、`u.lemma=0`}加进队列`db.add_nd`)

      ```
      db.sbase();
      ```

      <font size=3>`NOTE`: 在初始化hypothesis的过程中，`FOOT`/`MIDPOINT `/`INTERSECT `/`ONLINE`/`COLL `等commands可生成2点以上的线段，其中`ONLINE`/`COLL `会更新`db.all_ln`已有线段的点集；若存在几何表达的引用了该实例线段，则其该几何表达是实时更新的</font>

    - 更新几何信息库（执行`db.fixpoint()`：遍历现有的`db.all_nd`不断搜索新的predicate，`nd`通过`add_<cclass>()`绑定`nd.u`(`nd.u.co`，`nd.u.lemma`) 和 `nd.pred`)

      ```
      db.prove_fix();
      ```
      
      `NOTE`: 1.在search predicate的过程中，`db.split_ln`操作也会更新`db.all_ln`分割后的线段；2.search过的`nd`，其`nd.u.<cclass>.type`设置为1 
      
      ```
      nd.u.set_type(1);
      ```
      
    - `db.docc`判断结论`db.conc`是否已被推导出并存储于`db`，若存在则进行`bottom-up backward`得到证明路径

      ```
      if (db.docc()) {
          db.show_fproof();  // bottom-up backward
          if (db.all_nd.nx != null)
              return true;
      }
      ```

    - `bottom-up backward`具体实现 (注意代码中命名为`forw_pred`，可能会混淆)

      ```
      void show_fproof() {
          if (conc_xtrue()) {
              last_nd = all_nd;
              cp_pred(conc);  // 由执行完prove_fix后all_nd.nx已指向null，这里将conc作为all_nd新队首
              if (check_pred(last_nd)) { //"(The fact is trivially true)\r\n";
                  return;
              }
              do_pred(last_nd);  // 从db中查找conclusion
              forw_pred(last_nd);
      }
      ```

    - 以example1为例

      | 题目                                 | 题图                                                         |
      | ------------------------------------ | ------------------------------------------------------------ |
      | ![example1](https://github.com/Syarujianai/Java-Geometry-Expert/raw/master/md_figures/example1.png) | <img src="https://github.com/Syarujianai/Java-Geometry-Expert/raw/master/Junior%20Mathematics/example_1.JPG" alt="example_1" style="zoom:75%;" /> |

      > `db.sbase()`: 初始化`Prover.db.all_nd`为输入hypothesis

      ```
      - all_nd.nx
      	- A,B,D,G are collinear 
          - perp[C,D; A,B,D,G] 
          - plines[B,C,F; D,E] 
          - A,C,E are collinear 
          - B,C,F are collinear 
          - A,B,D,G are collinear 
          - ∠[CDE] = ∠[GFB] 
      ```

      > `db.prove_fix()`: 遍历几何信息库(`all_nd`队列)，通过BFS搜索对应`pred type`的新conclusion，conclusion通过`new_pr()`加入几何信息库
      >
      > `NOTE`: `db.all_nd`仍为队列，下面只是展开为BFS搜索树

      ```
      - A,B,D,G are collinear 
      - perp[C,D; A,B,D,G] 
      - plines[B,C,F; D,E] 
        - ∠[ADE] = ∠[ABC] (同位角, lemma2) 
          - congruent triangles[1.DAE.BAC] (st, AAA相似, lemma31) 
        - AB*AE = AD*AC (平行线比例分割线段, lemma3) 
          - congruent triangles[1.BAE.DAC] (st, lemma0) (TODO: 相似三角形点顺序没有对应上(sim_tri: st.dr=1出错)，导致搜索出错误的关系)
            - ∠[ACD] = ∠[AEB] (st, SSS相似, lemma33?) 
            - ∠[ADC] = ∠[ABE] (st, SSS相似, lemma33?) 
        - AB*DE = AD*BC (平行线比例分割线段, lemma3) 
        - AC*DE = AE*BC (平行线比例分割线段, lemma3) 
        - AB*CE = BD*AC (平行线比例分割线段, lemma3) 
        - AD*EC = DB*AE (平行线比例分割线段, lemma3) 
        - ∠[BED] = ∠[EBC] (同位角/内错角, lemma2) 
        - ∠[CDE] = ∠[DCB] (同位角/内错角, lemma2) 
        - ∠[AED] = ∠[ACB] (同位角/内错角, lemma2) 
        - ∠[FDE] = ∠[DFB] (同位角/内错角, lemma2) 
        - ∠[FED] = ∠[EFB] (同位角/内错角, lemma2) 
      - A,C,E are collinear 
      - B,C,F are collinear 
      - A,B,D,G are collinear 
      - ∠[CDE] = ∠[GFB] 
        - ∠[BCD] = ∠[BFG] (同位角, lemma181) 
          - congruent triangles[1.CBD.FBG] (st, AAA相似, lemma31) 
        - plines[F,G; C,D] (lemma166) 
          - perp[F,G; A,B,D,G] (平行垂直垂直, lemma4) 
          - BF*BD = BC*BG (tri BGF ~ tri BDC, lemma3) 
          - BF*CD = BC*FG (tri BGF ~ tri BDC, lemma3) 
          - BG*CD = BD*FG (tri BGF ~ tri BDC, lemma3) 
          - BF*GD = FC*BG (tri BGF ~ tri BDC, lemma3) 
          - BC*DG = CF*BD (tri BGF ~ tri BDC, lemma3) 
          - ∠[FDC] = ∠[DFG] (同位角/内错角, lemma2) 
          - ∠[GCD] = ∠[CGF] (同位角/内错角, lemma2) 
      ```

      > `db.show_fproof`(): 以conclusion为入口进行bottom-up backward
      >
      > `NOTE`: 第二层为展开后的`vlist`(条件)

      ```
      void show_fproof() {
          if (conc_xtrue()) {  // 结论是否被推出
              last_nd = all_nd;
              cp_pred(conc);  // 以conc变量初始化all_nd
              if (check_pred(last_nd)) {
                  return;
              }
              do_pred(last_nd);  // 根据conc的<pred type>搜索相应all_<pred type>队列并赋值给nd.u
              forw_pred(last_nd);  // bottom-up backward
          }
      }
      ```

      ```
      void forw_pred(cond co) {
          cond pr1, pr2, pr3;
          show_dtype = 0;
          all_nd.nx = co;
          last_nd = co;
          co.no = 1;
          co.nx = null;
          gno = 1;
      
          for (cond pr = all_nd.nx; pr != null; pr = pr.nx) {
      
              if (!isPFull() && !check_tValid(pr)) {
                  last_nd = all_nd;
                  all_nd.nx = null;
                  return;
              }
      
              if (pr.u.isnull()) {  //The fact is trivially true
                  if (show_detail && pr.pred == gib.CO_ACONG) {
                      forw_eqangle(pr);
                  }
                  continue;
              } else if ((pr1 = PCO(pr)) == null) {  // 获取cond.u.<pred type>.co，并赋值于pr1
                  pr.getRuleFromeFacts();  // 从几何表达cond.u.<pred type>.co中获取lemma，结果赋值于pr.rule 
                  continue;
              } else if (pr1.p[1] != 0) {
      
                  for (; pr1 != null; pr1 = pr1.nx) {  // 遍历pr的所有condition (pr1.nx)
                      if (pr1.pred == 0) {
                          continue;
                      }
                      if ((pr3 = fd_pred(pr1)) != null) {  // 若pr1已在`all_nd`中出现，赋值给pr3
                          pr.addcond(pr3);
                      } else {
                          do_pred(pr1);  // 将已经推理得到的几何事实赋值给pr1.u
                          if (pr1.u.isnull()) {  // obvious
                              pr.addcond(pr1);
                          } else if (PCO(pr1) == null) {  // hyp: pr1.u == null
                              pr.addcond(pr1);
                          } else {
                              cp_pred(pr1);  // 将pr1添加至`all_nd`,继续推导
                              pr1.no = last_nd.no;
                              pr.addcond(pr1);
                          }
                      }
                  }
                  pr.getRuleFromeFacts();
              } else {  // 所需conditions大于等于2
                  pr2 = pr1.nx;  /* pr0=last_nd; */
                  switch (pr.pred) {
                      case CO_COLL:
                          add_pred_coll(pr, pr1, pr2);
                          break;
                      case CO_PARA:// && (pr1.pred == CO_COLL || pr1.pred == CO_PARA)) {
                          add_pred_para(pr, pr1, pr2);  // 根据lemma选择新增的condition，并添加至`all_nd`,pr绑定rule (lemma<=43时，rule=lemma)
                          break;
                      case CO_ACONG:
                          add_pred_as(pr, pr1, pr2);
                          break;
                      case CO_TANG:
                          add_pred_at(pr, pr1, pr2);
                          break;
                      case CO_PERP:
                          add_pred_perp(pr, pr1, pr2);
                          break;
                      case CO_ATNG:
                          add_pred_atn(pr, pr1, pr2);
                          break;
                      case CO_CYCLIC:
                          add_pred_cr(pr, pr1, pr2);
                          break;
                      default: {
                          for (; pr1 != null; pr1 = pr1.nx) {
                              pr3 = fd_prep(pr1);
                              if (pr3 != null) {
                                  pr.addcond(pr3);
                              } else if ((pr3 = PCO(pr1)) == null) { //"(hyp)";
                                  pr.addcond(pr1);
                              } else {
                                  cp_pred(pr1);
                                  pr.addcond(last_nd);
                              }
                          }
                      }
                  }
              }
          }
      }
      ```

      ```
      - FG ⊥ AB
          - AB ⊥ CD
          - FG ∥ CD
      - FG ∥ CD
      	- ∠[BFG] = ∠[BCD]
      - ∠[BFG] = ∠[BCD]
          - ∠[BCD] = ∠[EDC]
          - ∠[BFG] = ∠[EDC]
      - ∠[BCD] = ∠[EDC]
          - BC ∥ DE
      ```

  

  ## Geosolver

  ### OCR调参

  由于geosolver会错误地将角标的弧线检测为圆，导至出现错误的交点 (`intersection_points`)，因而需要调整圆的检测阈值 

  ![error circle](https://github.com/Syarujianai/Java-Geometry-Expert/raw/master/md_figures/error circle.PNG)

  ```
  /* parameter.py */
  # These eps determine pixel coverage of each primitive.
  LINE_EPS = 7
  CIRCLE_EPS = 3
  PRIMITIVE_SELECTION_MIN_GAIN = 10
  ```

  

  ### 坐标点提取及符号匹配

  - 坐标点提取及匹配部分位于repo中的`geosolver/try2.py`，`Geometry_Extractor.parse_image_segments()`进行字母的模板匹配并返回bounding box`detected_char`，将geosolver提取的坐标点跟对应字母的bounding box进行匹配

  - geosolver的坐标点提取是通过segments的求交点得到的，因而坐标精度取决于segments检测的准确度，因而repo中也实现了基于haris角点检测的精确坐标提取，在完成符号模板匹配后用haris角点进行重匹配
  - 使用haris角点检测进行坐标提取需要在调用`GeometryImageParser.parse_image()`时设置`use_haris_centroids=True`

  ![corner1](https://github.com/Syarujianai/Java-Geometry-Expert/raw/master/geosolver-master/corner1.png)

  ![corner2](https://github.com/Syarujianai/Java-Geometry-Expert/raw/master/geosolver-master/corner2.png)

  ![corner3](https://github.com/Syarujianai/Java-Geometry-Expert/raw/master/geosolver-master/image.png)

  

  `NOTE`: 直角标记会影响提取坐标点的精度（表现为相邻的centroid偏向直角标记一侧）

  

  ### 可视化

  该部分实现分为两部分：

  - 基于规则匹配geosolver `graph_parse`中instances
  - 调用`graph_parse.display_instance`显示匹配到的instances (底层调用`opencv2`)

  `NOTE`: 调用`geosolver.diagram.get_instances.get_all_instances()`时获取多边形instances时，需要注释`geosolver/diagram/get_instances.py` 中的`polygon = FormulaNode(signatures[name.capitalize()], points)`，否则返回的polygon instance为`FormulaNode` type报错

  

##  Data Structures and Variables

- 类的依赖关系

  ```
  + wprover
  	+ GExpert  // 几何专家入口类
  	+ PanelProve1  // 窗口类
  	+ Gprover  // 装饰后的gprover
  	+ drawBase  // 画笔类
  		+ drawProcess
  	+ CClass  // 几何表达抽象类，无法实例化只能被继承，外部定义诸如符号化的操作对动态绑定CClass子类
  		+ CPoint
  		+ CAngle
  		+ CArrow
  		+ CPolygon
  		+ CText
  		+ CTrace
  		+ ... // 基本几何表达：C开头子类与GUI内action相关,而动作完成后以下述子类存进db
  		+ angles
  		+ anglet
  		+ angst
  		+ ...
  
  + gprover
  	+ gib  // 几何信息库类(geometric information base)，定义了信息库数据结构用到的所有静态变量
  		+ gddbase
  			+ gdd  // 定义了fixpoint用到的所有search函数
  				+ gdd_aux
  					+ gdd_bc
      + cond  // condition类，定义了单条条件/推导所需的所有元素
      + cclass  // 同wprover
      + gterm  // formal language化的题目
      + CST  // formal language的command libraries，根据HYP和SHOW的不同分为两类
      + Cm  // 关键字映射表
      + Prover  // 证明器类
      + Main2  // GDD证明入口类
  	
  ```



- `gprover.gib`变量定义

  | 后缀 | 解释                                                         | 对应的cclass子类 |
  | ---- | ------------------------------------------------------------ | ---------------- |
  | st   | similar triangle / congruent triangle                        | `sim_tri`        |
  | cg   | congruent segement，等长/比例线段ratio=t1/t2                 | `cong_seg`       |
  | cgs  | congruent segements                                          | `c_segs`         |
  | at   | 以垂足分割的垂线为边构成的角, 该类角给定了数值(用于应用勾股定理) | `anglet`         |
  | atn  | 互余角                                                       | `angtn`          |
  | as   | similar，等角                                                | `angles`         |
  | ast  | 多角相等                                                     | `angst`          |
  | tn   | 一组相互垂直的线段                                           | `t_line`         |
  | pn   | 一组相互平行的线段                                           | `p_line`         |
  | ra   | ratio segments，区别于比例线段（2条），为等比例线段对（4条） | `ratio_seg`      |
  | md   | mid point                                                    | `midpt`          |
  | cr   | circle                                                       | `a_cir`          |
  | pg   | polygon                                                      | `polygon`        |

  | 前缀 | 解释          |
  | ---- | ------------- |
  | cong | congruent全等 |
  | sim  | similar相似   |

  | 变量名                     | 解释                                                         | 类型                                                         |
  | -------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
  | `all_nd`                   | nd: next deduction                                           | `cond`                                                       |
  | `allcns`                   | cns: conclusions                                             | `cons[]`包括`ps`和`pss`，其中`ps`为conclusion中所有点的id，`pss`为其对应符号 |
  | `allpts`                   | pts: points                                                  | `Pro_point[]`包括点的坐标和id                                |
  | `all_xx`可配合上述前缀类推 | ...                                                          | ...                                                          |
  |                            |                                                              |                                                              |
  | `co_xy`                    | 临时condition database，`db.fixpoint()`内执行`add_<template>x()`（带x后缀）时读取，需要手动重置；`nd.u.<cclass>.co`会从中获取所需条件，以进行bottom-up backward (`Prover.forw_pred()`) | `cond`                                                       |
  | `co_db`                    | condition database，不同点在于执行`add_<template>()`（不带x后缀）读取，通过`add_codb`和`pop_codb`控制进出栈 | `cond`                                                       |
  | `tm_pr1`                   | 临时变量，`Prover.forw_pred`()中执行`add_pred`()时调用       | `cond`                                                       |
  | `test_ln`                  | 临时变量，类似的可依此类推                                   | `l_line`                                                     |
  | `conc`                     | conc: 待证明的conclusion                                     | `cond`                                                       |
  | `cons_no`                  | db中的conclusion数目                                         | `int`                                                        |
  | `pts_no`                   | db中点的数目                                                 | `int`                                                        |
  |                            |                                                              |                                                              |
  | `ZERO`                     | 容错等级0，用于角度比较的误差阈值，etc.                      | `double`                                                     |
  | `ZERO_TRUE`                | 容错等级1，用于ratio比较的误差阈值，etc.                     | `double`                                                     |
  | `ZERO_COLL`                | 容错等级2，用于带乘法的数值检测（但精度要求更高），etc.，    | `double`                                                     |
  | `ZERO_PRO`                 | 容错等级3，用于带乘法的数值检测，etc.，                      | `double`                                                     |
  |                            |                                                              |                                                              |
  | `P_STATUS`                 | 0：全角法                                                    | `int`                                                        |
  | `DEBUG`                    | 是否输出debug信息                                            | `boolean`                                                    |

  | 静态变量类别                              | 变量名                      | 解释                        | 类型/注释                                                    |
  | :---------------------------------------- | --------------------------- | --------------------------- | ------------------------------------------------------------ |
  | rules                                     | Rvalue                      | 是否使用对应rules           | `boolean`                                                    |
  |                                           | R_P_COLL~R_AG_BISECTOR_ATIO | 对应`GUI>lemma>GDD`引理1~43 | `int`                                                        |
  |                                           |                             |                             |                                                              |
  | predicate types（i.e., 给定条件类型）     | C_O_L                       | 线段                        | `int`                                                        |
  |                                           | C_O_P                       | 平行线                      |                                                              |
  |                                           | C_O_T                       | 垂线                        |                                                              |
  |                                           | C_O_B                       | 过三点作圆                  |                                                              |
  |                                           | C_O_A                       | 四边形                      |                                                              |
  |                                           | C_FOOT                      | 过某点作某线段的垂线        |                                                              |
  |                                           | C_CIRCLE                    | 以圆心、半径作圆            |                                                              |
  |                                           | C_O_C                       | 选择直径、圆心作圆          |                                                              |
  |                                           | C_CIRCUM                    | circumcentre，三角形外心    |                                                              |
  |                                           | C_O_R                       | 等长/比例线段               |                                                              |
  |                                           | C_SYM                       | 作某点于某线段的对称点      |                                                              |
  |                                           | C_R_TRI                     | 直角三角形                  |                                                              |
  |                                           | C_EQ_TRI                    | 等边三角形                  |                                                              |
  |                                           | C_R_TRAPEZOID               | 直角梯形                    |                                                              |
  |                                           | C_LOZENGE                   | 菱形                        |                                                              |
  |                                           | C_ICENT                     | incenter，三角形内心        |                                                              |
  |                                           | C_ORTH                      | orthocenter，三角形垂心     |                                                              |
  |                                           | C_CENT                      | centroid，三角形重心        |                                                              |
  |                                           | C_SANGLE                    | 指定角度                    |                                                              |
  |                                           | C_LC_TANGENT                | 线圆正切                    |                                                              |
  |                                           | C_CCTANGENT                 | 两圆相交弦                  |                                                              |
  |                                           | C_O_S                       | 圆(三点表示)上取一点        |                                                              |
  |                                           | C_O_AB                      | 角平分线上取一点            |                                                              |
  |                                           | C_O_D                       | 圆(两点表示)上取一点        |                                                              |
  |                                           | C_EQANGLE3P                 | 三角相等                    |                                                              |
  |                                           | C_COMPL_ANGLE               | 互余角                      |                                                              |
  |                                           | C_I_LL                      | 线线交于一点                | *I: intersection，未列出的关系可以此类推                     |
  |                                           | C_I_LP                      | 线与平行线交于一点          |                                                              |
  |                                           |                             |                             |                                                              |
  | conclusions（用于输入结论或backward推导） | CO_COLL                     | 共线                        | `int`                                                        |
  |                                           | CO_MIDP                     | 中点                        |                                                              |
  |                                           | CO_CONG                     | 等长线段                    |                                                              |
  |                                           | CO_ACONG                    | 等角                        |                                                              |
  |                                           | CO_TANGENT                  | 弦                          | *仅实现了面积法部分                                          |
  |                                           | CO_HARMONIC                 | 调和                        | *仅实现了面积法部分                                          |
  |                                           | CO_EQ                       | 等于某常量                  | *仅实现了面积法部分，详情阅读`Area.java`及`xterm.java`       |
  |                                           | CO_STRI                     | 相似三角形                  |                                                              |
  |                                           | CO_CTRI                     | 全等三角形                  |                                                              |
  |                                           | CO_PROD                     | 等比例线段对                |                                                              |
  |                                           | CO_INCENT                   | 三角形内心                  |                                                              |
  |                                           | CO_RATIO                    | 比例线段                    |                                                              |
  |                                           | CO_TANG                     | 给定角度                    |                                                              |
  |                                           | CO_NANG                     | 多等角                      |                                                              |
  |                                           | CO_NSEG                     | 多等长线段                  |                                                              |
  |                                           | CO_COMPL_ANGLE/CO_ATNG      | 互余角                      |                                                              |
  |                                           |                             |                             |                                                              |
  | 非退化条件(Non-degenerative Conditions)   | NDG_NEQ                     |                             | *ngd可参考[gclc_man.pdf](http://poincare.matf.bg.ac.rs/~janicic/gclc/) (chapter 6.4.3) |
  |                                           | NDG_COLL                    |                             |                                                              |
  |                                           | NDG_PARA                    |                             |                                                              |
  |                                           | NDG_PERP                    |                             |                                                              |
  |                                           | NDG_CYCLIC                  |                             |                                                              |
  |                                           | NDG_CONG                    |                             |                                                              |
  |                                           | NDG_ACONG                   |                             |                                                              |
  |                                           | NDG_NON_ISOTROPIC           |                             |                                                              |
  |                                           | NDG_TRIPLEPI                |                             |                                                              |
  |                                           |                             |                             |                                                              |
  | Inequality Predicates（i.e., 不等式条件） | IN_BETWEEN                  |                             | *不等式条件，这里仅预定义未进行实现                          |
  |                                           | IN_AG_INSIDE                |                             |                                                              |
  |                                           | IN_AG_OUTSIDE               |                             |                                                              |
  |                                           | IN_TRI_INSIDE               |                             |                                                              |
  |                                           | IN_PARA_INSIDE              |                             |                                                              |
  |                                           | IN_OPP_SIDE                 |                             |                                                              |
  |                                           | IN_SAME_SIDE                |                             |                                                              |
  |                                           | IN_PG_CONVEX                |                             |                                                              |

- 类型解释

  - condition类 (常用于`nd`和`co`)

    ```
    /* cond */
    public class cond {
        final public static int MAX_GEO = 16;
        protected int rule = 0;  // 证明该nd使用的引理，于`db.add_pred_xx()`时更新(`u.<cclass>.lemma`作为入口条件)
        public int pred;  // condition对应的predicate type
        public int no;  // condition id
        public int[] p;  // 该nd包含的几何表达所对应的坐标点id
        public ustruct u;  // 该nd包含的几何表达，midpt, l_line, etc.
        public cond nx, cd;  // next引用，用于`all_nd`
        public String sd = null;  // `db.show_allpred()`中调用
        public Vector vlist = null;  // `Prover.forw_pred()`中，通过`cond.add_cond()`添加所需conditions，用于`Prover.getProveHead()`
        public long dep = gib.depth;
    }
    ```

  - ustruct类

    ```
    /* ustruct */
    class ustruct {
        midpt md;
        l_line ln;
        p_line pn;
        t_line tn;
        a_cir cr;
        angles as;
        anglet at;
        angtn atn;
        sim_tri st;
        cong_seg cg;
        ratio_seg ra;
        polygon pg;
        l_list ns;
    }
    ```

  - 以等角`angles`为例 (`cclass`子类)

    ```
    public class angles extends cclass
    {
       // int type;  // NOTE: `angles`并没有`type`变量，常用于`l_line`类型的判断(两点线段type为0)或作为是否已search过该几何表达(某condition下)的判断
        int lemma;  // 在`db.sbase()`中初始化为0表示已知的hypothesis，而在`db.fixpoint()`中使用引理推导出的几何表达则会更新该项
        cond co;  // 推导出该几何表达(某condition下)，所需conditions，对于给定condition实例中使用`db.PCO()`获取所需conditions
        int sa;
        public l_line l1,l2, l3, l4;  // 对应一对等角的四条边
        angles nx;  // next引用，用于`all_as`
        int atp = 0;
    }`
    ```



#  Dev & Debug Tips

## Condition Database

用于更新`nd.u.<cclass>.co`，以进行bottom-up backward (`Prover.forw_pred()`)

- 使用`co_xy`

  ```
  /* 用法1 */
  angtn a1=add_atn(133,ln1,ln2,ls3[i],ls4[j]);  // 添加all_nd，并更新last_nd
  
  if(a1!=null){
  
      co_xy.nx=null;  // 需要从手动清空co_xy
  
      cond co=add_coxy(CO_ATNG);  // 所需条件1
  
      co.u.atn=new angtn(ln1,ln2,s1,s2);
  
      co=add_coxy(CO_ACONG);  // 所需条件2
  
      co.u.as=new angles(ls3[i],ls4[j],s3,s4);
  
      a1.co=co;  // 几何表达绑定所需条件
  
  }
  ```

  ```
  /* 用法2 */
  final t_line add_tx(int lm,l_line l1,l_line l) {
  
      // …
  
      tn1.lemma=lm;
  
      tn1.co=co_xy.nx;  // 几何表达绑定所需条件
  
      new_pr(CO_PERP);  // 添加all_nd，并更新last_nd
  
      last_nd.u.tn=tn1; 
  
      return tn1;
  
  }
  ```

- 使用`co_db`

  ```
  /* 以垂直为例 */
  
  // ...
  
  add_codb(CO_PERP, l1.pt[0], l1.pt[1], l2.pt[0], l2.pt[1], 0, 0, 0, 0);  // 所需条件1
  
  add_codb(CO_PARA, ln.pt[0], ln.pt[1], l2.pt[0], l2.pt[1], 0, 0, 0, 0); // 所需条件2
  
  add_tline(R_PT_T, ln.pt[0], ln.pt[1], l1.pt[0], l1.pt[1]);  // 几何元素绑定所需条件
  
  pop_codb();  // 条件2出栈
  
  pop_codb(); // 条件1出栈
  ```

- `fd_ln1`，注意两点与三点的区别

- 共线也可以使用`on_para`判定

  

## Debug Tips

- `ANAME`将点id转换为对应的symbol
- 数值检测是相关错误可以将`check_xx`函数的符号信息 (用上面提到的`ANAME()`符号化) 边打印出来边调参 (`gib.ZERO`)

- `IEDA Watches`可添加`Prover.getProveHead()`以实时刷新`all_nd.sd` (条件或推导的符号表示)



## 自定义predicate type

- e.g., `CO_COMPL_ANGLE`

- 可以在`CST.cst`与`CST.conclution`中添加输入条件类型 (条件/结论)，同时在`gib`中也添加于列表中对应序号的`pred type`和`conclusion`静态变量 (条件/结论)，最后在`gddbase.do_pd()`及`gdd_bc.do_pred()/forw_pred()`添加对应`pred type`的代码

- ps: 如果新增输入条件无法用已经有的`cclass`子类表达，则还需定义对应的`cclass`子类及`fo_<cclass>()`(found函数)

  

## para_as_type

关于`Prover.db.forw_pred()` `add_pred_para()`时，`case 166`内`para_as_type`的说明

(`recap `: lemma166，一组边平行，一组角相等，对应角的另一组边平行，具体可分为两种情况)

### 非平行四边形定理

- para_as_type 1:

  ```
  DE∥BC
  
  ∠CDE =  ∠GFB
  
  -> CD∥GF
  ```

![example_1](https://github.com/Syarujianai/Java-Geometry-Expert/raw/master/Junior%20Mathematics/example_1.JPG)

- para_as_type 2（`NOTE`:下例中CE、CD与AB、BF间仅有一交点时才成立）:  

  ```
  CE∥BF
  
  ∠CDE =  ∠GFB
  
  -> AB ∥ CD
  ```

  ![example_3](https://github.com/Syarujianai/Java-Geometry-Expert/raw/master/Junior%20Mathematics/example_3.JPG)

### 平行四边形定理

- para_as_type 3: 平行四边形

  ```
  BE∥FD
  
  ∠ADC=  ∠ABC
  
  -> AD∥ BC
  ```

  ![example_19](https://github.com/Syarujianai/Java-Geometry-Expert/raw/master/Junior%20Mathematics/example_19.JPG)



## 添加`as`或`atn`时边顺序规范及正确性说明

### 等角

- 在`add_ea_ln(l1, l2, l3, l4)`添加新的`as`时，需要保证等角所对应边的顺序均为顺时针或均为逆时针

  - 以lemma166为例，若l1/l2重合但边的顺序不同会导致错误的平行推理

    ![correctness_explain1](https://github.com/Syarujianai/Java-Geometry-Expert/raw/master/md_figures/correctness_explain1.png)

  - 以lemma145为例，若l1/l2垂直但边的顺序不同会导致错误的垂直推理

    ![correctness_explain2](https://github.com/Syarujianai/Java-Geometry-Expert/raw/master/md_figures/correctness_explain2.png)





### 互余角

- 在添加`atn`时应使用`split_ln`以角的顶点对线段进行分割，以避免在`Prover.db.forw_pred()`时无法辨识输入的互余角



## 坐标格式说明

- 以example1为例，正确的点坐标格式如下所示：

```
A(147.670157068+7,39.2879581152-24) B(27.2287234043+7,212.090425532-24) C(260.922018349+7,211.449541284-24) D(106.704347826+7,101.365217391-24) E(188.595238095+7,101.671428571-24) F(108.794117647+7,212.12745098-24) G(54.1244019139+7,173.827751196-24)
```

`NOTE`: 使用`gterm.writeAterm()`后保存的坐标后会带`+7` 、`-24`字样，若没有在`gterm.readAterm()`读取时会跳过y轴坐标



## 使用GUI添加测试样例

- 在GUI上完成尺规作图，然后左侧会自动生成program，通过`save_as_txt`可同时保存program和坐标

  

## 其它

- JGEX中，几何关系检测有二，check开头的是基于数值的检测，x开头的是基于几何关系库的检测

- `fd_ln1(int p1,int p2)`返回的`l_line`只能为2点



#  TODO

## 	JGEX

- 以example3为例：输入OCR得到的坐标时仍求解失败 -> 数值检测调参

- 以example1为例：搜索出全等三角形`[BAE.DAC]`时点顺序没有对应上导致`search_ct`时`st.dr=1`出错，导致搜索结果出错 (`∠[ACD] = ∠[AEB]`，`∠[ADC] = ∠[ABE]`)

- 以example21为例，垂直+等角的组合推导出另一组等角，但条件`∠[EGA] = ∠[ABE] + ∠[BEG]`由三角形外角定理推出，需要在`add_pred_as()`中定义这种pattern然后更改和添加所需的conditions

  ![example_21](https://github.com/Syarujianai/Java-Geometry-Expert/raw/master/Junior%20Mathematics/example_21.JPG)

  ![result_21](https://github.com/Syarujianai/Java-Geometry-Expert/raw/master/md_figures/result_21.PNG)

- 尺规作图parser，即从文本和图像得到尺规作图的program：

  复现PLDI2011 [paper](https://www.microsoft.com/en-us/research/publication/synthesizing-geometry-constructions/) 6.2节，即给定geosolver parse结果作为constraints，通过constraint optimazation得到坐标点；在通过simulator获得坐标点后，需要额外复现算法中search program部分，即从尺规作图library搜索出program

- 补角：修改现有`as`相关的`rules`以支持补角

- 角的关系：无法输入angle equation

- 平行线构成的同旁内角：无法推理同旁内角的互补的关系

- 角度计算：不支持某些内置特殊角 (e.g., 20°)

- 部分题目无法通过GUI进行尺规作图：手写或者优先完成parser

  

  ## Geosolver

- `parse_core`在可视化角时会显示外角

  ![visualize_error](https://github.com/Syarujianai/Java-Geometry-Expert/raw/master/md_figures/visualize_error.PNG)

- 题图分辨率过低时会匹配不到部分字母：不要使用截图）

- 使用 `matplotlib` API替换 `cv2.imshow()` 使得画布能够固定

