
import java.time.LocalDate;
import java.time.Month;
import java.time.format.DateTimeFormatter;
import java.time.temporal.TemporalAdjusters;
import java.util.HashMap;

import com.dassault_systemes.platform.restServices.MediaProviderJSON;
import com.dassault_systemes.platform.restServices.RestService;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.DELETE;
import jakarta.ws.rs.DefaultValue;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.QueryParam;
import jakarta.ws.rs.core.Context;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
@Path("/custom")
public class CustomService  extends RestService {
    @Path("/getReportData")
	@GET
	@Produces({ MediaType.APPLICATION_JSON, MediaProviderJSON.TYPE })
	@Consumes({ MediaType.APPLICATION_JSON, MediaProviderJSON.TYPE })
	public Response getReportData(@Context HttpServletRequest request, @QueryParam("type") @DefaultValue("") String type, @QueryParam("year") @DefaultValue("") String year, @QueryParam("groupBy") @DefaultValue("") String groupBy, @QueryParam("slice") @DefaultValue("") String slice) {
		matrix.db.Context context = this.getAuthenticatedContext(request, false);
        String startDate = "1/1/"+year;
        String endDate = "12/31/"+year;
		HashMap<String,HashMap<String,Integer>> response = CustomImplementation.getReport(context,type,startDate,endDate,groupBy,slice);
 		return Response.status(200).entity(response).build();
	}
    @Path("/getCellData")
	@GET
	@Produces({ MediaType.APPLICATION_JSON, MediaProviderJSON.TYPE })
	@Consumes({ MediaType.APPLICATION_JSON, MediaProviderJSON.TYPE })
	public Response getCellData(@Context HttpServletRequest request, @QueryParam("type") @DefaultValue("") String type, @QueryParam("year") @DefaultValue("") String year, @QueryParam("groupBy") @DefaultValue("") String groupBy, @QueryParam("slice") @DefaultValue("") String slice, @QueryParam("month") @DefaultValue("") String month, @QueryParam("groupval") @DefaultValue("") String groupval) throws Exception {
		try {			
			matrix.db.Context context = this.getAuthenticatedContext(request, false);
			DateTimeFormatter inputFormatter = DateTimeFormatter.ofPattern("M/d/yyyy");
			String startDate="";
			String endDate="";
			if("Monthly".equals(slice)){
				startDate = month+"/1/"+year;
				LocalDate localDate = LocalDate.parse(startDate, inputFormatter);
				endDate = localDate.with(TemporalAdjusters.lastDayOfMonth()).format(inputFormatter);
			}
			else{
				System.out.println("mkk: inside quater");
				int qyear = Integer.parseInt(year);
				int quarter = Integer.parseInt(month.substring(1));
				Month startMonth = Month.of((quarter - 1) * 3 + 1);
				LocalDate StartMonth = LocalDate.of(qyear, startMonth, 1);
				startDate = StartMonth.format(inputFormatter); 
				System.out.println(startDate);
				Month endMonth = Month.of(quarter * 3);
				LocalDate EndMonth = LocalDate.of(qyear, endMonth, 1).with(TemporalAdjusters.lastDayOfMonth());
				endDate = EndMonth.with(TemporalAdjusters.lastDayOfMonth()).format(inputFormatter);
				System.out.println(endDate);
			}
			Object response = CustomImplementation.getCellData(context,type,startDate,endDate,groupBy,slice,groupval);
			return Response.status(200).entity(response).build();	
		} catch (Exception e) {
			e.printStackTrace();
			throw e;
		}
	}
	@Path("/delete")
	@DELETE
	@Produces({ MediaType.APPLICATION_JSON, MediaProviderJSON.TYPE })
	@Consumes({ MediaType.APPLICATION_JSON, MediaProviderJSON.TYPE })
	public Response delete(@Context HttpServletRequest request, @QueryParam("ids") @DefaultValue("") String ids,@QueryParam("deletechild") @DefaultValue("") Boolean deletechild) throws Exception {
		matrix.db.Context context = this.getAuthenticatedContext(request, false);
		String[] arrIds = ids.split(",");
		CustomImplementation.delete(context,arrIds,deletechild);
 		return Response.status(200).entity("{}").build();
	}
	@Path("/recycle")
	@GET
	@Produces({ MediaType.APPLICATION_JSON, MediaProviderJSON.TYPE })
	@Consumes({ MediaType.APPLICATION_JSON, MediaProviderJSON.TYPE })
	public Response recycle(@Context HttpServletRequest request, @QueryParam("ids") @DefaultValue("") String ids) throws Exception {
		String[] arrIds = ids.split(",");
		matrix.db.Context context = this.getAuthenticatedContext(request, false);
		CustomImplementation.recycle(context,arrIds);
 		return Response.status(200).entity("{}").build();
	}
    @Path("/permanentlydelete")
	@DELETE
	@Produces({ MediaType.APPLICATION_JSON, MediaProviderJSON.TYPE })
	@Consumes({ MediaType.APPLICATION_JSON, MediaProviderJSON.TYPE })
	public Response permanentlydelete(@Context HttpServletRequest request, @QueryParam("ids") @DefaultValue("") String ids) throws Exception {
		matrix.db.Context context = this.getAuthenticatedContext(request, false);
		String[] arrIds = ids.split(",");
		CustomImplementation.permanentlydelete(context,arrIds);
 		return Response.status(200).entity("{}").build();
	}
	@Path("/getMyRecycleBin")
	@GET
	@Produces({ MediaType.APPLICATION_JSON, MediaProviderJSON.TYPE })
	@Consumes({ MediaType.APPLICATION_JSON, MediaProviderJSON.TYPE })
	public Response getMyRecycleBin(@Context HttpServletRequest request, @QueryParam("type") @DefaultValue("") String type) throws Exception {
		matrix.db.Context context = this.getAuthenticatedContext(request, false);
		Object Binlist = CustomImplementation.getMyRecycleBin(context,type);
 		return Response.status(200).entity(Binlist).build();
	}
	@Path("/getChildren")
	@GET
	@Produces({ MediaType.APPLICATION_JSON, MediaProviderJSON.TYPE })
	@Consumes({ MediaType.APPLICATION_JSON, MediaProviderJSON.TYPE })
	public Response getCAs(@Context HttpServletRequest request, @QueryParam("id") @DefaultValue("") String id ) throws Exception {
		matrix.db.Context context = this.getAuthenticatedContext(request, false);
		Object Children = CustomImplementation.getChildren(context,id);
 		return Response.status(200).entity(Children).build();
	}
}

