import java.util.ArrayList;
import java.util.HashMap;

import com.matrixone.apps.domain.util.FrameworkException;
import com.matrixone.apps.domain.util.FrameworkUtil;
import com.matrixone.apps.domain.util.MqlUtil;

import matrix.db.Context;
import matrix.util.StringList;
public class CR_Implementation{
    public static ArrayList<String> getProjects(Context context){
        ArrayList<String> projects = new ArrayList<>();
        try {
            String sProjects = MqlUtil.mqlCommand(context, "temp query bus $1 $2 $3 select $4 dump $5", "PnOProject", "*", "*", "id", "|");
            System.out.println("MKK sProjects: "+sProjects);
            StringList slProjects = FrameworkUtil.split(sProjects, "\n");
            for(String sProject:slProjects){
                StringList slProjectData = FrameworkUtil.split(sProject, "|");
                System.out.println("MKK slProjectData: "+slProjectData);
                projects.add(slProjectData.get(1));
            }
        } catch (FrameworkException e) {
            e.printStackTrace();
        }
        return projects;
    }
    public static ArrayList<HashMap<String,String>> getCRS(Context context, String project){
        ArrayList<HashMap<String,String>> CRs = new ArrayList<>();
        try {
            String sCRs = MqlUtil.mqlCommand(context, "temp query bus $1 $2 $3 where $4 select $5 $6 $7 $8 dump $9", "Change Request", "*", "*", "project=='"+project+"'", "current", "attribute[Title]","originated", "owner", "|");
            System.out.println("MKK sCRs: "+sCRs);
            StringList slCRs = FrameworkUtil.split(sCRs, "\n");
            for(String sCR:slCRs){
                StringList slCRData = FrameworkUtil.split(sCR, "|");
                System.out.println("MKK slCRData: "+slCRData);
                HashMap<String,String> CR=new HashMap<>();
                CR.put("id", slCRData.get(1));
                CR.put("title", slCRData.get(4));
                CR.put("current", slCRData.get(3));
                CR.put("originated", slCRData.get(5));
                CR.put("owner", slCRData.get(6));
                CRs.add(CR);
            }
        } catch (FrameworkException e) {
            e.printStackTrace();
        }
        return CRs;
    }
}