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
    public static void viz_proof(cond pr_head, Hashtable<String, Integer> visited_pr_sd){
        cond pr = pr_head;
        if(pr.nx != null)
            viz_proof(pr.nx, visited_pr_sd);

        /* visualize proof */
        int count_append = 0;
        StringBuilder builder = new StringBuilder();
        boolean is_encounter_lemma = false, is_dup = false;
        if((pr.sd.contains("∥")) && (pr.u.pn != null) && (pr.u.pn.lemma == 166) && (pr.vlist.size() == 2))
            is_encounter_lemma = true;

        if(is_encounter_lemma){
            boolean is_reverse_order = false, is_variant_type = false, is_skip_para=false;

            /* get a glimpse of conclusion (already to deduct) */
            String[] type_patterns = pr.sd.split(" ∥ ");
            // String type_pattern_rev = new StringBuffer(type_pattern).reverse().toString();

            /* prepare initial string for resolve */
            String vertex = "", angle_intermediate = "", angle_known = "";
            StringBuilder another_builder = new StringBuilder();
            String[] primitives_pn = new String[]{};
            String[] primitives_an = new String[]{};

            /* detect order and type, and store primitives */
            for (int i = 0; i < pr.vlist.size(); i++) {
                cond v = (cond) pr.vlist.get(i);

                /* store omitted proof step of lemma */
                if (v.sd.contains("∥")) {
                    primitives_pn = v.sd.split(" ∥ ");
                    if (i == 1) {
                        is_reverse_order = true;
                    }
                } else if (v.sd.contains("∠")) {
                    primitives_an = v.sd.split(" = ");
                    angle_known = primitives_an[0];

                    /* detect variant type */
                    for (String p : primitives_an) {
                        for (int j = 0; j< 2; j++){
                            if(p.contains(type_patterns[j]) && j == 1)
                                is_variant_type = true;
                        }
                    }
                }
            }

            /* prepare components of proof steps */
            if (is_variant_type) {
                if (primitives_an[1].contains(primitives_pn[1])) {
                    another_builder.append(primitives_an[1].substring(2, 4));
                } else {
                    another_builder.append(primitives_an[1].substring(3, 5));
                }
                another_builder.reverse();
                vertex = primitives_an[0].substring(4, 5);
            } else {
                if (primitives_an[0].contains(primitives_pn[0])) {
                    another_builder.append(primitives_an[0].substring(3, 5));
                } else {
                    another_builder.append(primitives_an[0].substring(2, 4));
                }
                vertex = primitives_an[1].substring(2, 3);
            }
            another_builder.append(vertex);
            angle_intermediate = another_builder.toString();
            another_builder.append("] = "+primitives_an[1]);  // DCB] = ∠[CDE]

            if(is_reverse_order){
                for (int i = pr.vlist.size()-1; i >= 0; i--){  // reverse
                    cond v = (cond) pr.vlist.get(i);

                    if (visited_pr_sd.containsKey(v.sd)){
                        if(v.sd.contains("∥")){
                            is_skip_para = true;
                        }
                        builder.append("又 ");
                        continue;
                    }

                    if(count_append == 0){
                        builder.append("∵ "+v.sd);

                        if(is_skip_para){
                            /* resolve proof step of lemma (after skipped parallel) */
                            System.out.println("∴ ∠["  + another_builder.toString());

                            System.out.println(builder.toString());  // angle
                            builder.setLength(0);

                            builder.append( "∴ " + angle_known + " = " + "∠[" + angle_intermediate + "]");  // final angles relationship
                        }else {
                            System.out.println(builder.toString());  // parallel
                            builder.setLength(0);

                            /* resolve proof step of lemma (after parallel) */
                            System.out.println("∴ ∠["  + another_builder.toString());
                        }
                    }else{
                        if(count_append == 1){
                            builder.append("又 ∵ "+v.sd+"\n");
                            builder.append( "∴ " + angle_known + " = " + "∠[" + angle_intermediate + "]");  // final angles relationship
                        } else{
                            builder.append(", "+v.sd);
                        }
                    }
                    count_append += 1;
                }
            }else{
                for (int i = 0; i < pr.vlist.size(); i++) {
                    cond v = (cond) pr.vlist.get(i);

                    if (visited_pr_sd.containsKey(v.sd)){
                        builder.append("又 ");
                        continue;
                    }

                    if(count_append == 0){
                        builder.append("∵ "+v.sd);
                        /* resolve proof step of lemma */
                        System.out.println(builder.toString());
                        System.out.println("∴ ∠["  + another_builder.toString());
                        builder.setLength(0);
                    }else{
                        if(count_append == 1){
                            builder.append("又 ");
                            builder.append("∵ "+v.sd+"\n");
                            builder.append( "∴ " + angle_known + " = " + "∠[" + angle_intermediate + "]");
                        } else{
                            builder.append(", "+v.sd);
                        }
                    }
                    count_append += 1;
                }
            }
        }else{
            for (int i = 0; i < pr.vlist.size(); i++) {
                cond v = (cond) pr.vlist.get(i);

                if (visited_pr_sd.containsKey(v.sd)){
                    is_dup = true;
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

        String pr_v  = builder.toString();
        if(is_dup){
            pr_v = "又 " + pr_v;
        }
        System.out.println(pr_v);

        if (!visited_pr_sd.containsKey(pr.sd))
            visited_pr_sd.put(pr.sd, 1);
        System.out.println("∴ "+pr.sd);
    }

    public static void main(String[] args) {
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
            // gt.readAterm(new DataInputStream (new FileInputStream(chooser.getSelectedFile())));
            gt.readAterm(new BufferedReader(new FileReader(chooser.getSelectedFile())));
            gib.initRulers();
            Prover.set_gterm(gt);
            Boolean t = Prover.prove();
            System.out.println(t);
            cond pr_head = Prover.getProveHead();

            Hashtable<String, Integer> visited_pr_sd = new Hashtable<String, Integer>();
            viz_proof(pr_head, visited_pr_sd);

            System.out.println(t);

        } catch (IOException ee) {
        }
        //CMisc.print(Cm.s2077);
    }
}
