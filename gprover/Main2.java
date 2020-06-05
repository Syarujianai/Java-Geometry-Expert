/**
 * Created by IntelliJ IDEA.
 * User: Ye
 * Date: 2006-2-18
 * Time: 21:26:51
 * To change this template use File | Settings | File Templates.
 */
package gprover;

import javax.swing.*;
import java.io.*;
import java.nio.Buffer;
import java.util.Hashtable;
import java.util.Vector;


public class Main2 {
    public static void println_wrapper(String proof, StringBuilder outs, int out_mode){
        if(out_mode == 1){
            outs.append(proof+"\n");
        }else {
            System.out.println(proof);
        }
    }

    public static void visualize_proof(cond pr_head, Hashtable<String, Integer> visited_pr_sd, int out_mode, StringBuilder outs){
        cond pr = pr_head;
        if(pr.nx != null)
            visualize_proof(pr.nx, visited_pr_sd, out_mode, outs);

        /* visualize proof */
        int count_append = 0, count_skip = 0;
        StringBuilder builder = new StringBuilder();
//        boolean is_encounter_lemma = false;
//        if((pr.sd.contains("∥")) && (pr.u.pn != null) && (pr.u.pn.lemma == 166) && (pr.vlist.size() == 2))
//            is_encounter_lemma = true;
//
//        if(is_encounter_lemma){
//            boolean is_reverse_order = false, is_variant_type = false, is_skip_para=false;
//
//            /* get a glimpse of conclusion (already to deduct) */
//            String[] type_patterns = pr.sd.split(" ∥ ");
//            // String type_pattern_rev = new StringBuffer(type_pattern).reverse().toString();
//
//            /* prepare initial string for resolve */
//            String vertex = "", angle_intermediate = "", angle_known = "";
//            StringBuilder another_builder = new StringBuilder();
//            String[] primitives_pn = new String[]{};
//            String[] primitives_an = new String[]{};
//
//            /* detect order and type, and store primitives */
//            for (int i = 0; i < pr.vlist.size(); i++) {
//                cond v = (cond) pr.vlist.get(i);
//
//                /* store omitted proof step of lemma */
//                if (v.sd.contains("∥")) {
//                    primitives_pn = v.sd.split(" ∥ ");
//                    if (i == 1) {
//                        is_reverse_order = true;
//                    }
//                } else if (v.sd.contains("∠")) {
//                    primitives_an = v.sd.split(" = ");
//                    angle_known = primitives_an[0];
//
//                    /* detect variant type */
//                    for (String p : primitives_an) {
//                        for (int j = 0; j< 2; j++){
//                            if(p.contains(type_patterns[j]) && j == 1)
//                                is_variant_type = true;
//                        }
//                    }
//                }
//            }
//
//            /* prepare components of proof steps */
//            if (is_variant_type) {
//                if (primitives_an[1].contains(primitives_pn[1])) {
//                    another_builder.append(primitives_an[1].substring(2, 4));
//                } else {
//                    another_builder.append(primitives_an[1].substring(3, 5));
//                }
//                another_builder.reverse();
//                vertex = primitives_an[0].substring(4, 5);
//            } else {
//                if (primitives_an[0].contains(primitives_pn[0])) {
//                    another_builder.append(primitives_an[0].substring(3, 5));
//                } else {
//                    another_builder.append(primitives_an[0].substring(2, 4));
//                }
//                vertex = primitives_an[1].substring(2, 3);
//            }
//            another_builder.append(vertex);
//            angle_intermediate = another_builder.toString();
//            another_builder.append("] = "+primitives_an[1]);  // DCB] = ∠[CDE]
//
//            if(is_reverse_order){
//                for (int i = pr.vlist.size()-1; i >= 0; i--){  // reverse
//                    cond v = (cond) pr.vlist.get(i);
//
//                    if (visited_pr_sd.containsKey(v.sd)){
//                        if(v.sd.contains("∥")){
//                            is_skip_para = true;
//                        }
//                        builder.append("又 ");
//                        continue;
//                    }
//
//                    if(count_append == 0){
//                        builder.append("∵ "+v.sd);
//
//                        if(is_skip_para){
//                            /* resolve proof step of lemma (after skipped parallel) */
//                            println_wrapper("∴ ∠["  + another_builder.toString(), outs, out_mode);
//
//                            println_wrapper(builder.toString(), outs, out_mode);  // angle
//                            builder.setLength(0);
//
//                            builder.append("∴ " + angle_known + " = " + "∠[" + angle_intermediate + "]");  // final angles relationship
//                        }else {
//                            println_wrapper(builder.toString(), outs, out_mode);  // parallel
//                            builder.setLength(0);
//
//                            /* resolve proof step of lemma (after parallel) */
//                            println_wrapper("∴ ∠["  + another_builder.toString(), outs, out_mode);
//                        }
//                    }else{
//                        if(count_append == 1){
//                            builder.append("又 ∵ "+v.sd+"\n");
//                            builder.append( "∴ " + angle_known + " = " + "∠[" + angle_intermediate + "]");  // final angles relationship
//                        } else{
//                            builder.append(", "+v.sd);
//                        }
//                    }
//                    count_append += 1;
//                }
//            }else{
//                for (int i = 0; i < pr.vlist.size(); i++) {
//                    cond v = (cond) pr.vlist.get(i);
//
//                    if (visited_pr_sd.containsKey(v.sd)){
//                        builder.append("又 ");
//                        continue;
//                    }
//
//                    if(count_append == 0){
//                        builder.append("∵ "+v.sd);
//                        /* resolve proof step of lemma */
//                        println_wrapper(builder.toString(), outs, out_mode);
//                        println_wrapper("∴ ∠["  + another_builder.toString(), outs, out_mode);
//                        builder.setLength(0);
//                    }else{
//                        if(count_append == 1){
//                            builder.append("又 ");
//                            builder.append("∵ "+v.sd+"\n");
//                            builder.append( "∴ " + angle_known + " = " + "∠[" + angle_intermediate + "]");
//                        } else{
//                            builder.append(", "+v.sd);
//                        }
//                    }
//                    count_append += 1;
//                }
//            }
//        }else{
            for (int i = 0; i < pr.vlist.size(); i++) {
                cond v = (cond) pr.vlist.get(i);

                if (visited_pr_sd.containsKey(v.sd)){
                    count_skip += 1;
                    continue;
                }

                if(count_append == 0){
                    builder.append("∵ "+v.sd);
                }else{
                    builder.append(", "+v.sd);
                }
                count_append += 1;
            }
        // }

        if(count_append != 0){
            String pr_v  = builder.toString();
            if(count_skip > 0){
                pr_v = "又 " + pr_v;
            }
            println_wrapper(pr_v, outs, out_mode);
        }


        if (!visited_pr_sd.containsKey(pr.sd))
            visited_pr_sd.put(pr.sd, 1);

        builder.setLength(0);
        builder.append("∴ "+pr.sd);
        switch (pr.rule) {
            case gib.R_AA_STRI:
                builder.append(" (ASA)");
            case gib.R_PARALLELOGRAM:
                builder.append(" (parallelgram)");
        }
        println_wrapper(builder.toString(), outs, out_mode);
    }

    public static String parse_and_prove_problem(int problem_id, int out_mode){

//        String user_directory = System.getProperty("user.dir");
//        String user_directory = "C:\\Users\\DM\\Desktop\\code\\geo\\Java-Geometry-Expert\\output\examples\";
        String user_directory = "C:\\Users\\DM\\Desktop";
        String sp = System.getProperty("file.separator");
        String dr = user_directory + sp + "Junior Mathematics\\";
        String dr_file = dr + String.format("example_%d.txt", problem_id);
        String dr_ex_file = dr + String.format("positions_%d.txt", problem_id);
        String dr_compound_file = dr + String.format("combined_%d.txt", problem_id);
        File file = new File(dr_file);
        File ex_file = new File(dr_ex_file);
        File compound_file = new File(dr_compound_file);

        /* preproccessing */
        try {
            if (!file.exists()) return "Files could not be found";
            else {
                if (ex_file.exists() && !compound_file.exists()) {
                    /* combine files */
                    BufferedWriter bw = new BufferedWriter(new FileWriter(compound_file));
                    BufferedReader br_1 = new BufferedReader(new FileReader(file));
                    BufferedReader br_2 = new BufferedReader(new FileReader(ex_file));
                    String line;
                    while ((line = br_1.readLine()) != null) {
                        bw.write(line);
                        bw.newLine();
                    }
                    while ((line = br_2.readLine()) != null) {
                        bw.write(line);
                        bw.newLine();
                    }
                    bw.flush();
                    bw.close();
                }
            }
        } catch (IOException ee){
        }
//        JFileChooser chooser = new JFileChooser();
//        chooser.setCurrentDirectory(new File(dr));
//        int result = chooser.showOpenDialog(null);
//        if (result == JFileChooser.CANCEL_OPTION) return "Files could not be found";
        gterm gt = new gterm();
        StringBuilder outs = new StringBuilder();

        /* read gterm, prove and visualize */
        try {
            /* read gterm */
            // gt.readAterm(new DataInputStream (new FileInputStream(chooser.getSelectedFile())));
            // gt.readAterm(new BufferedReader(new FileReader(chooser.getSelectedFile())));
            if(compound_file.exists()){
                gt.readAterm(new BufferedReader(new FileReader(compound_file)));
            }else{
                gt.readAterm(new BufferedReader(new FileReader(file)));
            }

            /* prove */
            gib.initRulers();
            Prover.set_gterm(gt);
            Boolean is_proved = Prover.prove();
            System.out.println((is_proved? "proved: true": "proved: false"));

            /* visualize proof steps */
            cond pr_head = Prover.getProveHead();
            Hashtable<String, Integer> visited_pr_sd = new Hashtable<String, Integer>();
            visualize_proof(pr_head, visited_pr_sd, out_mode, outs);
        } catch (IOException ee) {
            ee.printStackTrace();
        }

        return outs.toString();
    }

    public static void main(String[] args) {
        int[] problem_ids = new int[] {
             1, 3, 6, 8, 12, 19, 21, 28, 29, 33, 34, 35, 36, 49
        };

        for (int i = 0; i< problem_ids.length; i++) {
            try{
                if (problem_ids[i] != 3) continue;
                System.out.printf("id: %d \n", problem_ids[i]);
                parse_and_prove_problem(problem_ids[i], 0);
                System.out.println();
            } catch (NullPointerException ee) {
                ee.printStackTrace();
                continue;
            }
        }
        //CMisc.print(Cm.s2077);
    }
}
