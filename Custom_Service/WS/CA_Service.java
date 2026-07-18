import java.util.ArrayList;
import java.util.HashMap;

import com.dassault_systemes.platform.restServices.MediaProviderJSON;
import com.dassault_systemes.platform.restServices.RestService;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.DefaultValue;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.QueryParam;
import jakarta.ws.rs.core.Context;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

@Path("/ca")
public class CA_Service extends RestService {
	@Path("/getCAData")
	@GET
	@Produces({ MediaType.APPLICATION_JSON, MediaProviderJSON.TYPE })
	@Consumes({ MediaType.APPLICATION_JSON, MediaProviderJSON.TYPE })
	public Response getCAData(@Context HttpServletRequest request, @QueryParam("startDate") @DefaultValue("") String startDate, @QueryParam("endDate") @DefaultValue("") String endDate, @QueryParam("groupBy") @DefaultValue("") String groupBy) {
		matrix.db.Context context = this.getAuthenticatedContext(request, false);
		ArrayList<String> projects = CustomImplementation.getCAData(context,startDate,endDate,groupBy);
 		return Response.status(200).entity(projects).build();
	}
	@Path("/getCAS")
	@GET
	@Produces({ MediaType.APPLICATION_JSON, MediaProviderJSON.TYPE })
	@Consumes({ MediaType.APPLICATION_JSON, MediaProviderJSON.TYPE })
	public Response getCAs(@Context HttpServletRequest request, @QueryParam("project") @DefaultValue("") String project) {
		matrix.db.Context context = this.getAuthenticatedContext(request, false);
		System.out.println("Project is : "+project);
		ArrayList<HashMap<String,String>> CRs = CustomImplementation.getCRS(context,project);
 		return Response.status(200).entity(CRs).build();
	}
}
