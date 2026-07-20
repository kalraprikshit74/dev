import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import com.matrixone.apps.domain.DomainObject;
import com.matrixone.apps.domain.util.FrameworkException;
import com.matrixone.apps.domain.util.FrameworkUtil;
import com.matrixone.apps.domain.util.MapList;
import com.matrixone.apps.domain.util.MqlUtil;

import matrix.db.Context;
import matrix.util.StringList;
public class CustomImplementation{
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
    public static ArrayList<HashMap<String,Object>> getCAData(Context context,String startDate,String endDate,String groupBy){
        startDate = startDate.replaceAll("-","/");
        endDate = endDate.replaceAll("-","/");
        ArrayList<HashMap<String,Object>> response = new ArrayList<>();
        HashMap<String,Integer> counts = new HashMap<>();
        List<String> colors = Arrays.asList("#ff415b", "#2ecc71", "#3498db", "#f1c40f", "#e67e22", "#9b59b6", "#1abc9c", "#34495e", "#2c3e50", "#7f8c8d", "#8e44ad", "#c0392b", "#ff7675", "#74b9ff", "#a29bfe", "#ffeaa7", "#fab1a0", "#55efc4","#dfe6e9", "#2d3436");
        try {
            String whereClause = "originated >'" +startDate + "' && originated<'" + endDate+"'";
            StringList selects = new StringList();
            selects.add(groupBy);
            MapList CAs = DomainObject.findObjects(context,"Change Action","*","*","*","*",whereClause, null, false, selects, ((short)0),"*","");
            for(Object ca:CAs){
                HashMap objectMap = (HashMap)ca;
                String groupByValue = (String)objectMap.get(groupBy);
                if(counts.containsKey(groupByValue))
                    counts.put(groupByValue, counts.get(groupByValue)+1);
                else
                    counts.put(groupByValue, 1);
            }
            int i =0;
            for(String key: counts.keySet()){
                HashMap<String,Object> data = new HashMap<>();
                data.put("label", key);
                data.put("value", counts.get(key));
                data.put("color", colors.get(i++));
                response.add(data);
            }
        }
         catch (FrameworkException e) {
            e.printStackTrace();
        }
        return response;
    }
    public static MapList getCAs(Context context,String startDate,String endDate,String groupBy, String groupByValue) throws FrameworkException{
        startDate = startDate.replaceAll("-","/");
        endDate = endDate.replaceAll("-","/");
        try {
            String whereClause = "originated >'" +startDate + "' && originated<'" + endDate+"' && "+groupBy+"=='"+groupByValue+"'";
            StringList selects = new StringList();
            selects.add("type");
            selects.add("name");
            selects.add("revision");
            selects.add("current");
            selects.add("attribute[severity]");
            selects.add("owner");
            MapList CAs = DomainObject.findObjects(context,"Change Action","*","*","*","*",whereClause, null, false, selects, ((short)0),"*","");
            return CAs;   
        }
         catch (FrameworkException e) {
            e.printStackTrace();
            throw e;
        }
    }
}