import streamlit as st
from config.knowledge_based_app import knowledge_based_app
from config.machine_learning_app import machine_learning_app
from pathlib import Path
from models.machine_learning.bert_with_lexicon import BertWithLexicon

CWD = Path(__file__).parents[0]
CSS_FILE_PATH = CWD / Path('./config/styles.css')

def main():
    st.set_page_config(page_title="مشروع NLP", page_icon="🌐", layout="wide")

    # تحميل CSS المخصص
    with open(CSS_FILE_PATH) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # التنقل في الشريط الجانبي
    st.sidebar.title("لائحة البرامج")
    app_mode = st.sidebar.selectbox("اختر برنامج", ["نظرة عامة", "برنامج خمن الكلمة التالية (Knowledge Based)", "برنامج تحديد اللهجات (Machine Learning)"])
    
    if app_mode == "نظرة عامة":
        overview()
    elif app_mode == "برنامج خمن الكلمة التالية (Knowledge Based)":
        knowledge_based_app()
    elif app_mode == "برنامج تحديد اللهجات (Machine Learning)":
        machine_learning_app()

def overview():
    st.title("نظرة عامة على المشروع")
    
    st.markdown("""
    <div class="section">
        <h2>ملخص المشروع</h2>
        <p>يتضمن هذا المشروع تطبيقين رئيسيين:</p>
        <ol>
            <li><strong>برنامج خمن الكلمة التالية (Knowledge Based)</strong>: يستخدم نموذج n-gram للتنبؤ بالكلمة التالية في جملة معينة باستخدام مجموعة بيانات MADAR.</li>
            <p>نموذج n-gram يُستخدم لتحليل تسلسل الكلمات والتنبؤ بالكلمة التالية بناءً على تكرار الأنماط النحوية في النصوص المدخلة. يعتمد النموذج على تحليل الن-غرامات (n-grams) التي تتألف من n كلمة متتابعة.</p>
            <li><strong>برنامج تحديد اللهجات (Machine Learning)</strong>: يستخدم نموذج BERT مع المعجم لتحديد اللهجة العربية لنص معين باستخدام مجموعة بيانات MADAR lexicon.</li>
            <p>نموذج BERT متعدد اللغات مُدرب مسبقًا على البيانات متعددة اللغات من ويكيبيديا. يستخدم النموذج لمعالجة النصوص العربية وتحديد اللهجة باستخدام ميزات معجمية مدمجة. النموذج يُستخدم لتصنيف النصوص إلى لهجات عربية مختلفة بناءً على مجموعة بيانات MADAR lexicon.</p>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section">
        <h2>التراخيص والمراجع</h2>
        <h3>التراخيص</h3>
        <p>رخصة استخدام مجموعة بيانات MADAR</p>
        <p>حقوق الطبع والنشر (c) 2018-2022 جامعة كارنيجي ميلون وجامعة نيويورك أبوظبي. جميع الحقوق محفوظة.</p>
        <p>يتم منحك ترخيصًا لاستخدام ونسخ هذه المجموعة وموادها التوثيقية لأغراض البحث الداخلي والتقييم فقط، بدون رسوم وبدون توقيع اتفاقية ترخيص، عند تنزيلك للمجموعة، وبذلك توافق على ما يلي:</p>
        <ul>
            <li>ستظهر إشعار حقوق الطبع والنشر أعلاه، وهذه الفقرة والفقرات الثلاث التالية بشكل بارز في جميع النسخ الداخلية والتعديلات.</li>
            <li>لا تُمنح حقوق الترخيص الفرعي أو التوزيع الإضافي لهذا البرنامج.</li>
            <li>لا تُمنح حقوق تعديل هذه المجموعة.</li>
            <li>لا تُمنح حقوق نقل هذا الترخيص.</li>
        </ul>
        <p>يرجى الاتصال بمركز نقل التكنولوجيا وإنشاء المشاريع بجامعة كارنيجي ميلون، 4615 شارع فوربس، الجناح 302، بيتسبرغ، PA 15213 - هاتف 412.268.7393، للحصول على فرص الترخيص التجاري، أو لمزيد من التوزيع، أو حقوق التعديل أو الترخيص.</p>
        <p>تم إنشاؤه بواسطة Houda Bouamor، Nizar Habash، Mohammad Salameh، Wajdi Zaghouani، Owen Rambow، Dana Abdulrahim، Ossama Obeid، Salam Khalifa، Fadhl Eryani، Alexander Erdmann و Kemal Oflazer.</p>
        <p>لا تتحمل جامعة كارنيجي ميلون أو جامعة نيويورك، أو موظفوهم، أو وكلاؤهم أو الأمناء ("جماعيًا "أطراف جامعة كارنيجي ميلون/جامعة نيويورك") أي مسؤولية تجاه أي طرف عن الأضرار المباشرة، غير المباشرة، الخاصة، العرضية، أو التبعية من أي نوع، بما في ذلك الأرباح المفقودة، الناشئة عن أي مطالبة ناتجة عن استخدامك لهذه المجموعة وموادها التوثيقية، حتى إذا تم إبلاغ أي من أطراف جامعة كارنيجي ميلون/جامعة نيويورك بإمكانية حدوث مثل هذه المطالبة أو الضرر.</p>
        <p>جامعة كارنيجي ميلون/جامعة نيويورك تخلي مسؤوليتها عن أي ضمانات من أي نوع بخصوص المجموعة، بما في ذلك، على سبيل المثال لا الحصر، عدم الانتهاك، الضمانات الضمنية للتسويق والملاءمة لغرض معين، أو دقة أو فائدة، أو اكتمال البرنامج. يتم توفير البرنامج ومواد التوثيق المصاحبة له، إن وجدت، هنا بالكامل "كما هي". لا توجد التزامات على جامعة كارنيجي ميلون لتوفير مزيد من التوثيق، الصيانة، الدعم، التحديثات، التحسينات، أو التعديلات.</p>
        <p>إذا استخدمت هذا المورد، يرجى الاستشهاد بـ:</p>
        <p>Bouamor, Houda, Nizar Habash, Mohammad Salameh, Wajdi Zaghouani, Owen Rambow, Dana Abdulrahim, Ossama Obeid, Salam Khalifa, Fadhl Eryani, Alexander Erdmann و Kemal Oflazer. "مجموعة بيانات MADAR اللهجات العربية والمعجم". في وقائع المؤتمر الدولي للموارد اللغوية والتقييم (LREC 2018)، ميازاكي، اليابان، 2018.</p>
        <h3>المراجع</h3>
        <p>
            Bouamor, Houda, et al. "The MADAR Arabic Dialect Corpus and Lexicon." <a href="http://www.lrec-conf.org/proceedings/lrec2018/pdf/351.pdf">PDF</a> في وقائع المؤتمر الدولي للموارد اللغوية والتقييم (LREC 2018)، ميازاكي، اليابان، 2018.<br>
            Devlin, Jacob, et al. "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding." arXiv preprint arXiv:1810.04805 (2018). <a href="https://arxiv.org/pdf/1810.04805.pdf">PDF</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section">
        <h2>مشروع جامعة جدة</h2>
        <p>هذا المشروع مُقدَّم لمقرر "CCAI 413 Natural Language Processing" بجامعة جدة.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
