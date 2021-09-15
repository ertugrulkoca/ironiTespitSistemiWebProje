using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlClient;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace software_proje.Controllers
{
    public class IndexController : Controller
    {
        public ActionResult Index()
        {
            return View();
        }

        public class Sonuc
        {
            public string Text
            {
                get;
                set;
            }
        }

        [HttpPost]
        public JsonResult AjaxPostCall(Sonuc sonuc)
        {
            Sonuc result = new Sonuc
            {
                Text = sonuc.Text,
                
            };
            SqlConnection con = new SqlConnection("Data Source=.;Initial Catalog=SoftwareProje;Integrated Security=True; MultipleActiveResultSets=True;");
            SqlCommand cmd = con.CreateCommand();
            cmd.CommandText = "Execute savedata @text";
            cmd.Parameters.Add("@text", SqlDbType.VarChar, 250).Value = sonuc.Text;
            con.Open();
            cmd.ExecuteNonQuery();
            con.Close();
            return Json(result, JsonRequestBehavior.AllowGet);


        }
    }
}