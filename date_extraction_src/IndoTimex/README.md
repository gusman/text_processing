# IndoTimex
Temporal expression extraction system, including temporal expression recognition and normalization, for Indonesian language, written in Python.

###Requirements
* Python 2.7 or higher
* Java Runtime Environment (JRE) 1.7.x or higher
* [TimeNorm for Indonesian language](https://github.com/paramitamirza/timenorm-id) (.jar is provided in `lib/`)
 
###Usage
_! The input file(s) must be in the [TimeML annotation format](http://www.timeml.org/site/index.html) !_
```
python python TimexExtraction.py dir_name [options]        or
python python TimexExtraction.py file_name [options]

options: -o output_dir_name/file_name (default: dir_path/dir_name_Timex/ for directory and file_path/file_name_timex.tml for file)
```   
The output file(s) will be a TimeML document annotated with temporal expressions (TIMEX3 tags).

#####To convert TimeML file(s) to HTML for better viewing
```
python python ConvertToHTML.py dir_name [options]        or
python python ConvertToHTML.py file_name [options]

options: -o output_dir_name/file_name (default: dir_path/dir_name_HTML/ for directory and file_path/file_name.html for file)
```   

###Modules
IndoTimex contains two main modules:

1. **Timex recognition**, a finite state transducer (FST) to recognize temporal expressions and their types (based on the TimeML standard, i.e. DATE, DURATION, TIME and SET). The complete FST can be seen in [`lib/fst/timex.pdf`](https://github.com/paramitamirza/IndoTimex/blob/master/lib/fst/timex.pdf) (minimized and drawn with [OpenFST](http://www.openfst.org/)).
2. **Timex normalization**, an extension of [TimeNorm](https://github.com/bethard/timenorm), a library for normalizing the values of temporal expressions (based on the ISO 8601 standard) using synchronous context free grammars, for Indonesian language. To run the timex normalizer: `java -jar ./lib/timenorm-id-0.9.2-jar-with-dependencies.jar ./lib/id.grammar`.
 
#####Publication
Paramita Mirza. 2015. **Recognizing and Normalizing Temporal Expressions in Indonesian Texts**. *(to appear) In Proceedings of the Conference of the Pacific Association for Computational Linguistics (PACLING 2015)*, Bali, Indonesia, May. [pdf]

#####Dataset
The dataset for development and evaluation phases of the system is available in `dataset/`, comprising 75 news articles taken from www.kompas.com.

_! Whenever making reference to this resource please cite the paper in the Publication section. !_

###Demo
The online demo is available at [http://paramitamirza.ml/indotimex/](http://paramitamirza.ml/indotimex/).

###Contact
For more information please contact [Paramita Mirza](http://paramitopia.com/about/) (paramita@fbk.eu).
