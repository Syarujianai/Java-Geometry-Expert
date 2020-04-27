/**
 * Created by IntelliJ IDEA.
 * User: Ye
 * Date: 2006-2-18
 * Time: 21:26:51
 * To change this template use File | Settings | File Templates.
 */
package gprover;

import com.sun.org.apache.xerces.internal.util.SynchronizedSymbolTable;
import org.omg.CORBA.portable.InputStream;

import javax.swing.*;
import javax.swing.filechooser.FileFilter;
import java.io.*;
import java.util.HashSet;
import java.util.Hashtable;
import java.util.Set;


public class Main2 {
    public static void viz_proof(cond pr_head, Hashtable<String, Integer> has_sd){
        cond pr = pr_head;
        if(pr.nx != null)
            viz_proof(pr.nx, has_sd);

        /* visualize proof */
        int count_append = 0;
        StringBuilder builder = new StringBuilder();
        boolean encountered_lemma = false;
        if((pr.sd.contains("∥")) && (pr.u.pn != null) && (pr.u.pn.lemma == 166))
            encountered_lemma = true;

        if(encountered_lemma){
            String vertex = "", angle_intermediate = "", angle_known = "";
            StringBuilder another_builder = new StringBuilder();
            for (int i = pr.vlist.size()-1; i >= 0; i--){  // reverse
                cond v = (cond) pr.vlist.get(i);

                /* resolve proof step of lemma */
                if(v.sd.contains("∥")) {
                    String[] symbols = v.sd.split(" ∥ ");
                    vertex = symbols[0].substring(1);  // store vertex B (of FB) firstly

                }else if(v.sd.contains("∠")){
                    String[] symbols = v.sd.split(" = ");
                    angle_known = symbols[0];
                    another_builder.append(symbols[1].substring(2, 4)).reverse();  // reverse: CD -> DC
                    another_builder.append(vertex);
                    angle_intermediate = another_builder.toString();
                    another_builder.append("] = "+symbols[1]);  // DCB] = ∠[CDE]
                    System.out.println("∴ ∠["  + another_builder.toString());  // print redundant proof step secondly
                }

                if (has_sd.containsKey(v.sd)){
                    builder.append("又 ");
                    continue;
                }

                if(count_append == 0){
                    builder.append("∵ "+v.sd);
                    /* resolve proof step of lemma */
                    System.out.println(builder.toString());
                    builder.setLength(0);
                }else{
                    if(count_append == 1){
                        builder.append("又 ");
                        builder.append("∵ "+v.sd+"\n");
                        builder.append( "∴ " + angle_known + " = " + "∠[" + angle_intermediate);
                    } else{
                        builder.append(", "+v.sd);
                    }
                }
                count_append += 1;
            }
        }else{
            for (int i = 0; i < pr.vlist.size(); i++) {
                cond v = (cond) pr.vlist.get(i);

                if (has_sd.containsKey(v.sd)){
                    builder.append("又 ");
                    continue;
                }

                if(count_append == 0){
                    builder.append("∵ "+v.sd);
                }else{
                    builder.append(", "+v.sd);
                }
                count_append += 1;
            }
        }

        System.out.println(builder.toString());

        if (!has_sd.containsKey(pr.sd))
            has_sd.put(pr.sd, 1);
        System.out.println("∴ "+pr.sd);
    }

    public static void main(String[] args) {

//    final public static int CM_EX_PARA = 1;
//    final public static int CM_EX_ORTH = 2;
//    final public static int CM_EX_SIMSON = 3;
//    final public static int CM_EX_SQ = 4;
//    final public static int CM_EX_PAPPUS = 5;
//    final public static int CM_EX_PEDAL = 6;
//    final public static int CM_EX_MIQ1 = 7;

        String user_directory = System.getProperty("user.dir");
        String sp = System.getProperty("file.separator");
        // String dr = user_directory + sp + "ex";
        String dr = user_directory + sp + "output\\examples\\Junior Mathematics\\";
        JFileChooser chooser = new JFileChooser();
        chooser.setCurrentDirectory(new File(dr));
        int result = chooser.showOpenDialog(null);
        if (result == JFileChooser.CANCEL_OPTION) return;
        gterm gt = new gterm();
        try {
            // File file_1 = chooser.getSelectedFile();
            // gt.readAterm(new DataInputStream (new FileInputStream(chooser.getSelectedFile())));
            gt.readAterm(new BufferedReader(new FileReader(chooser.getSelectedFile())));
            gib.initRulers();
            Prover.set_gterm(gt);
            // Prover.run();
            Boolean t = Prover.prove();
            System.out.println(t);
            cond pr_head = Prover.getProveHead();

            Hashtable<String, Integer> has_sd = new Hashtable<String, Integer>();
            viz_proof(pr_head, has_sd);

            System.out.println(t);
//            gdd_bc db = new gdd_bc();
//            db.init_dbase();
//            db.setExample(gt);
//            db.sbase();
//            db.fixpoint();
//            db.show_fproof();


        } catch (IOException ee) {
        }

        //CMisc.print(Cm.s2077);
    }
}
