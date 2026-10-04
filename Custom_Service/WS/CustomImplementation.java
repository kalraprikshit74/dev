import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.temporal.IsoFields;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import com.matrixone.apps.domain.DomainConstants;
import com.matrixone.apps.domain.DomainObject;
import com.matrixone.apps.domain.util.ContextUtil;
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
            if(!"current".equals(groupBy))
                groupBy = "attribute["+groupBy+"]";
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
                System.out.println("keys:"+key);
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
            if(!"current".equals(groupBy))
                groupBy = "attribute["+groupBy+"]";
            String whereClause = "originated >'" +startDate + "' && originated<'" + endDate+"' && "+groupBy+"=='"+groupByValue+"'";
            System.out.println("MKDebug: whereClause:"+whereClause);
            StringList selects = new StringList();
            selects.add("type");
            selects.add("name");
            selects.add("revision");
            selects.add("current");
            selects.add("attribute[Category of Change]");
            selects.add("owner");
            MapList CAs = DomainObject.findObjects(context,"Change Action","*","*","*","*",whereClause, null, false, selects, ((short)0),"*","");
            return CAs;   
        }
         catch (FrameworkException e) {
            e.printStackTrace();
            throw e;
        }
    }
    public static List<HashMap<String, Object>> getCATimeSeries(Context context, String startDate, String endDate){
        List<HashMap<String, Object>> result = new ArrayList<>();    
        try{   
            HashMap<String,Integer> originatedCounts = new HashMap<>();
            HashMap<String,Integer> completedCounts = new HashMap<>();
            DateTimeFormatter inputFormatter = DateTimeFormatter.ofPattern("M/d/yyyy h:mm:ss a");
            DateTimeFormatter outputFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
            startDate = startDate.replaceAll("-","/");
            endDate = endDate.replaceAll("-","/");
            String sWhere = "originated >'" +startDate + "' && originated<'" + endDate+"'";
            System.out.println("MKDebug sWhere: "+sWhere);
            String sCAs = MqlUtil.mqlCommand(context, "temp query bus $1 $2 $3 where $4 select $5 $6 dump $7","Change Action","*","*",sWhere,"state[Complete].actual","originated","|");
            StringList slCAs = FrameworkUtil.split(sCAs, "\n");
            System.out.println("MKDebug slCAs: "+slCAs);
            for(String sca:slCAs){
                StringList slCAData = FrameworkUtil.split(sca, "|");
                String completed = slCAData.get(3);
                String originated = slCAData.get(4);
                originated = LocalDateTime.parse(originated, inputFormatter).withDayOfMonth(1).format(outputFormatter);
                originatedCounts.putIfAbsent(originated, 0);
                originatedCounts.put(originated, originatedCounts.get(originated)+1);
                if(!completed.isBlank()){
                    completed = LocalDateTime.parse(completed, inputFormatter).withDayOfMonth(1).format(outputFormatter);
                    completedCounts.putIfAbsent(completed, 0);
                    completedCounts.put(completed, completedCounts.get(completed)+1);
                }
                System.out.println("originatedcount"+originatedCounts);
                System.out.println("completedcount"+completedCounts);                

            }

        for (Entry<String, Integer> entry : originatedCounts.entrySet()) {
            HashMap<String, Object> map = new HashMap<String, Object>();
            map.put("date", entry.getKey());
            map.put("type", "created");
            map.put("value", entry.getValue());
            result.add(map);
        }

        for (Entry<String, Integer> entry : completedCounts.entrySet()) {
            HashMap<String, Object> map = new HashMap<String, Object>();
            map.put("date", entry.getKey());
            map.put("type", "resolved");
            map.put("value", entry.getValue());
            result.add(map);
        }
        System.out.println("MKDebug result:"+result);
        } catch (FrameworkException e) {
            e.printStackTrace();
        }
        return result;
    }
     public static HashMap<String,HashMap<String,Integer>> getReport(Context context, String type,String startDate,String endDate,String groupBy,String slice){
        HashMap<String,HashMap<String,Integer>> report = new HashMap<>();
        try {
            DateTimeFormatter DATE_FORMATTER = DateTimeFormatter.ofPattern("M/d/yyyy h:mm:ss a");
            String sWhere = "originated >='" +startDate + "' && originated<='" + endDate+"'";
            String sObjects = MqlUtil.mqlCommand(context, "temp query bus $1 $2 $3 where $4 select $5 $6 dump $7",type, "*", "*",sWhere, groupBy, "originated", "|");
            System.out.println("MKK sReports: "+sObjects);
            StringList slObjects = FrameworkUtil.split(sObjects, "\n");
            for (String sReport : slObjects) {
                StringList slObjectData = FrameworkUtil.split(sReport, "|");
                String state = slObjectData.get(3);
                String sOriginated = slObjectData.get(4);
                LocalDateTime dateTime = LocalDateTime.parse(sOriginated, DATE_FORMATTER);
                String monthKey = dateTime.getMonth().toString();
                if(!"Monthly".equals(slice))
                    monthKey = "Q"+dateTime.get(IsoFields.QUARTER_OF_YEAR);
                System.out.println("slice: "+slice+" monthKey: "+monthKey+" sOriginated: "+sOriginated);
                report.putIfAbsent(monthKey, new HashMap<>());
                HashMap<String,Integer> monthReport = report.get(monthKey);
                monthReport.putIfAbsent(state, 0);
                monthReport.put(state, monthReport.get(state)+1);
            }

        } catch (FrameworkException e) {
            e.printStackTrace();
        }
        return report;
    }
    public static MapList getCellData(Context context, String type,String startDate,String endDate,String groupBy,String slice,String groupval) throws Exception{
        try {
            String sWhere = "originated >='" +startDate + "' && originated<='" + endDate+"' && "+groupBy+"=="+groupval;
            StringList selects = new StringList();
            selects.add(DomainConstants.SELECT_TYPE);
            selects.add(DomainConstants.SELECT_NAME);
            selects.add(DomainConstants.SELECT_REVISION);
            selects.add(DomainConstants.SELECT_DESCRIPTION);
            selects.add(DomainConstants.SELECT_PHYSICAL_ID);
            MapList data = DomainObject.findObjects(context,type,"*","*","*","*",sWhere, null, false, selects, ((short)0),"*","");
            return data;
        } catch (FrameworkException e) {
            e.printStackTrace();
            throw e;
        }
    }

public static void delete(Context context, String[] ids, Boolean deletechild) throws Exception {
    StringList selects = new StringList();
    selects.add(DomainConstants.SELECT_PHYSICAL_ID);
    selects.add(DomainConstants.SELECT_PROJECT);
    
    MapList mlRoots = DomainObject.getInfo(context, ids, selects);
    
    for (Object map : mlRoots) {
        Map data = (Map) map;
        System.out.println(data);
        
        String physicalid = (String) data.get(DomainConstants.SELECT_PHYSICAL_ID);
        String cs = (String) data.get(DomainConstants.SELECT_PROJECT);
        
        if ("RecycleBin".equals(cs)) {
            continue;
        }
        
        DomainObject doProduct = DomainObject.newInstance(context, physicalid);
        
        if (deletechild) {
            StringList relationshipList = new StringList();
            try {
                MapList childs = doProduct.getRelatedObjects(context, "*", "VPMReference", selects, relationshipList, false, true, (short) 0, "", "", 0);
                System.out.println("MKK data childs:" + childs);
                
                for (Object child : childs) {
                    if (child instanceof Map) {
                        Map<?, ?> objectMap = (Map<?, ?>) child;
                        Object physicalIdObj = objectMap.get(DomainConstants.SELECT_PHYSICAL_ID);
                        String phyidChild = physicalIdObj != null ? physicalIdObj.toString() : null;
                        
                        System.out.println("MKK data project:" + cs);
                        System.out.println("MKK data physicalID:" + phyidChild);
                        
                        String command = "mod bus $1 project $2 $3 $4 $5 $6";
                        MqlUtil.mqlCommand(context, command, phyidChild, "RecycleBin", "XP_VPMReference_Ext.OriginalCS", cs, "XP_VPMReference_Ext.DeletedBy", context.getUser());
                        System.out.println("Product deleted");
                    }
                }
                
                String command = "mod bus $1 project $2 $3 $4 $5 $6";
                MqlUtil.mqlCommand(context, command, physicalid, "RecycleBin", "XP_VPMReference_Ext.OriginalCS", cs, "XP_VPMReference_Ext.DeletedBy", context.getUser());
                
            } catch (FrameworkException e) {
                e.printStackTrace();
                throw e;
            }
        } else {
            try {
                System.out.println("Checking related objects for physical id: " + physicalid);
                String command = "mod bus $1 project $2 $3 $4 $5 $6";
                MqlUtil.mqlCommand(context, command, physicalid, "RecycleBin", "XP_VPMReference_Ext.OriginalCS", cs, "XP_VPMReference_Ext.DeletedBy", context.getUser());
                
            } catch (FrameworkException e) {
                e.printStackTrace();
                throw e;
            }
        }
    }
}
    public static void recycle(Context context, String[] ids) throws Exception{
        try {
            for(String id:ids){
            DomainObject doProduct = DomainObject.newInstance(context,id);
            String originalcs = doProduct.getInfo(context, "attribute[XP_VPMReference_Ext.OriginalCS]");
            System.out.println(originalcs);
            String command = "mod bus $1 project $2 $3 $4 $5 $6";
            MqlUtil.mqlCommand(context, command, id, originalcs,"XP_VPMReference_Ext.OriginalCS", "","XP_VPMReference_Ext.DeletedBy","");            
            }
        } catch (FrameworkException e) {
            e.printStackTrace();
            throw e;
        }
    }
        public static void permanentlydelete(Context context, String[] ids) throws Exception{
        try {
            DomainObject.deleteObjects(context,ids);
        } catch (FrameworkException e) {
            e.printStackTrace();
            throw e;
        }
    }
    public static MapList getMyRecycleBin(Context context,String type) throws FrameworkException{
        try {
            String sWhere = "project=='RecycleBin' && to[VPMInstance]=='FALSE' && attribute[XP_VPMReference_Ext.DeletedBy]=='"+context.getUser()+"'";
            System.out.println(sWhere);
            ContextUtil.pushContext(context);
            StringList selects = new StringList();
            selects.add("attribute[PLMEntity.V_Name]");
            selects.add("type");
            selects.add("name");
            selects.add("revision");
            selects.add("current");
            selects.add("title");
            selects.add("physicalid");
            MapList Binlist = DomainObject.findObjects(context,type,"*","*","*","*",sWhere, null, false, selects, ((short)0),"*","");
            System.out.println(Binlist);
            return Binlist;   
        }
         catch (FrameworkException e) {
            e.printStackTrace();
            throw e;
        }
        finally{
            ContextUtil.popContext(context);
        }
    }

    public static MapList getChildren(Context context, String id) throws FrameworkException {
        StringList selects = new StringList();
        selects.add(DomainConstants.SELECT_PHYSICAL_ID);
        selects.add(DomainConstants.SELECT_PROJECT);
        selects.add(DomainConstants.SELECT_NAME);
        selects.add(DomainConstants.SELECT_REVISION);
        selects.add("attribute[PLMEntity.V_Name]");
        selects.add(DomainConstants.SELECT_TYPE);
        selects.add(DomainConstants.SELECT_CURRENT);
        StringList relationshipList = new StringList();
        try {
            ContextUtil.pushContext(context);
            DomainObject doProduct = DomainObject.newInstance(context, id);
            MapList children = doProduct.getRelatedObjects(context, "*", "VPMReference", selects, relationshipList,
                    false, true, (short) 1, "", "", 0);
            System.out.println("MKK data childs:" + children);
            return children;

        } catch (FrameworkException e) {
            e.printStackTrace();
            throw e;
        } finally {
            ContextUtil.popContext(context);
        }
    }
}