import com.dassault_systemes.platform.restServices.ModelerBase;

import jakarta.ws.rs.ApplicationPath;
@ApplicationPath("/CustomService")
public class CustomModeler extends ModelerBase {
	@Override
	public Class<?>[] getServices() {
		return new Class<?>[] {
			CR_Service.class
		};
	}

}
