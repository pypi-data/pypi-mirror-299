#include <algorithm>
#include "source_characterization.h"
#include "bessel.h"
#include "particle_generator.h"
#include "function_statistics.h"
#include "bm_wiggler_radiation.h"
#include "function_digitizer.h"
#include "trajectory.h"
#include "flux_density.h"
#include "spectra_debug.h"

#ifdef __NOMPI__
#include "mpi_dummy.h"
#else
#include "mpi.h"
#endif

#define MAXARGK1312 10.0
#define MAXARGSINC 30.0
#define ANGLEINTERVAL 0.05

SourceCharacterization::SourceCharacterization(double ephoton, 
    SpectraSolver &spsolver, int wlayer, bool zerodiv)
	: SpectraSolver(spsolver)
{
	int Nwiggler = 0, nh;
	double epsilon;
	m_dUmin = 0;

	if(m_isund){
		m_isidealund = !m_srcb[fielderr_]  && !m_srcb[phaseerr_] && m_srcsel[segment_type_] == NoneLabel;
	    if(m_srctype == FIGURE8_UND || m_srctype == VFIGURE8_UND){
		    nh = (int)floor(2.0*m_conf[hfix_]+0.5);
	    }
		else{
	        nh = (int)floor(m_conf[hfix_]+0.5);
		}
		double e1st = GetE1st();
		epsilon = (ephoton/(double)nh/e1st-1.0)*(double)(m_N*nh);
	}
	else{
		m_isidealund = false;
	}
	if(m_isbm){
		m_issinglebm = !m_srcb[bmtandem_];
	}
	else{
		m_issinglebm = false;
	}

	if(m_iswiggler){
		Nwiggler = m_N;
	}
	m_wigner = new WignerFunction(m_acclevel, Nwiggler, m_isidealund, m_isoddpole, m_calcstatus, wlayer);
	if(wlayer >= 0){
		m_calcstatus->ResetCurrentStep(wlayer);
	}

	m_wavelength = wave_length(ephoton);
	m_coefWDF = m_gamma/m_wavelength;
	m_coefWDF *= m_coefWDF;
	m_coefWDF *= COEF_ALPHA/1.0E+15*m_AvCurr/QE; 
		// /m^2/rad^2/100%BW -> /mm^2/mrad^2/0.1%BW
	m_penergy = ephoton;

	if(m_isidealund){
		double divxy[2], sizexy[2];
		GetNaturalSource(ephoton, divxy, sizexy);
		m_dqduv = 2.0*divxy[0];
		m_dXYdUV = sizexy[0];
		m_coefExy = (double)m_N/m_wavelength/m_gamma2;
		m_esigma = EnergySpreadSigma()*(double)(m_N*nh);
		f_AssignEFieldUnd(epsilon, nh, m_N);
	}
	else if(m_issinglebm || m_iswiggler){
		double ec = GetCriticalEnergy();
		double epsilon = ephoton/ec*0.75;
		m_ecritical = ec;
		epsilon = pow(epsilon, 1.0/3.0);
		double deltau = m_conf[horizacc_]*1.0e-3*m_gamma*epsilon;
		m_dqduv = 1.0/(epsilon*m_gamma);
		m_coefExy = 2.0/sqrt(3.0)/PI*epsilon;
		m_esigma = 0.0;
		if(m_iswiggler){
			double ke = m_Kxy[1][1];
			deltau = min(deltau, 2.0*ke*epsilon);
			double amp = ke*m_lu/PI2/m_gamma;
			ke *= epsilon;
			ke *= ke;
			m_dXYdUV = amp/ke/2.0;
			f_AssignEFieldWiggler(epsilon, deltau, true);
			m_dUmin = ke/4.0;
		}
		else{
			double bendr = GetOrbitRadius();
			m_dXYdUV = bendr*0.5*m_dqduv*m_dqduv;
			f_AssignEFieldBM(epsilon, deltau);
			m_dUmin = 1.0;
		}
	}
	else{
		m_esigma = EnergySpreadSigma();
		m_dqduv = 1.0/m_gamma;
		m_dXYdUV = m_wavelength*m_gamma/PI2;
		m_coefExy = 1.0/m_gamma;

		if(m_isund){
			double gt2uv, hDelta;
			m_gtrange[0] = m_gtrange[1] = f_GTmaxU(epsilon, nh, m_N, &gt2uv, &hDelta);
		}
		else{
			for (int j = 0; j < 2; j++){
				m_gtrange[j] = m_confv[gtacc_][j];
			}
		}
	}

	double sigmauv[2], sigmaUV[2], alpha[2], betaw, sxy2, spxy2, eta2, etad2;
	for(int j = 0; j < 2; j++){
		if(zerodiv){
			betaw = m_accv[beta_][j];
		}
		else{
			betaw = m_accv[beta_][j]/(1.0+m_accv[alpha_][j]*m_accv[alpha_][j]);
		}
		eta2 = EnergySpreadSigma()*m_accv[eta_][j]; eta2 *= eta2;
		etad2 = EnergySpreadSigma()*m_accv[etap_][j]; etad2 *= etad2;
		if(m_confb[zeroemitt_]){
			sxy2 = spxy2 = 0;
		}
		else{
			sxy2 = m_emitt[j]*betaw+eta2;
			spxy2 = m_emitt[j]/betaw+etad2;
		}
		m_sigmaxy[j] = sqrt(sxy2);
		if(zerodiv){
			sigmauv[j] = 0.0;
		}
		else{
			sigmauv[j] = sqrt(spxy2)/m_dqduv;
		}
		sigmaUV[j] = sqrt(sxy2)/m_dXYdUV;
		if(m_confb[zeroemitt_] || zerodiv){
			alpha[j] = 0;
		}
		else{
			alpha[j] = m_accv[alpha_][j]*m_emitt[j]/spxy2*m_dqduv/m_dXYdUV;
		}
	}
	if(zerodiv){
		sigmaUV[0] = max(sigmaUV[0], m_dUmin);

	}
	else if(contains(m_calctype, menu::wigner) && (m_isbm || m_iswiggler)){
		int smlevel = (int)floor(0.5+m_conf[xsmooth_]);
		sigmaUV[0] = max(sigmaUV[0], m_dUmin*(double)(1<<(smlevel-1)));
	}

	m_wigner->AssignCondition(sigmauv, sigmaUV, alpha);
}

SourceCharacterization::~SourceCharacterization()
{
	delete m_wigner;
}

void SourceCharacterization::GetPhaseSpaceProfile(int type, 
		double fixpoint[], double rangeini[], double rangefin[], int meshr[],
		vector<vector<double>> *xyarray, vector<vector<double>> *W,
		FluxDensity *fluxdens, int rank, int mpiprocesses, bool skipalloc,
		double *duv, int netgt,
		vector<vector<vector<complex<double>>>> *ExFnearp,
		vector<vector<vector<complex<double>>>> *EyFnearp)
{
	double uvini[2], uvfin[2], UVfix[2], uvfix[2], coef[2], xyini[2], xyfin[2], dxy[2];
	int mesh[2], idxy[2];

	UVfix[0] = fixpoint[WignerUVPrmU]/m_dXYdUV;
	UVfix[1] = fixpoint[WignerUVPrmV]/m_dXYdUV;
	uvfix[0] = fixpoint[WignerUVPrmu]/m_dqduv;
	uvfix[1] = fixpoint[WignerUVPrmv]/m_dqduv;

	switch(type){
		case WignerFuncTypeXY:
			idxy[0] = WignerUVPrmU;
			idxy[1] = WignerUVPrmV;
			coef[0] = coef[1] = m_dXYdUV;
			break;
		case WignerFuncType4DX:
		case WignerFuncType2DX:
		case WignerFuncType3DX:
			idxy[0] = WignerUVPrmU;
			idxy[1] = WignerUVPrmu;
			coef[0] = m_dXYdUV;
			coef[1] = m_dqduv;
			break;
		default:
			idxy[0] = WignerUVPrmV;
			idxy[1] = WignerUVPrmv;
			coef[0] = m_dXYdUV;
			coef[1] = m_dqduv;
			break;
	}
	for(int j = 0; j < 2; j++){
		uvini[j] = rangeini[idxy[j]]/coef[j];
		uvfin[j] = rangefin[idxy[j]]/coef[j];
		mesh[j] = meshr[idxy[j]];
		xyini[j] = rangeini[idxy[j]];
		xyfin[j] = rangefin[idxy[j]];
		if(mesh[j] > 1){
			dxy[j] = (xyfin[j]-xyini[j])/(double)(mesh[j]-1);
		}
		else{
			dxy[j] = 0.0;
		}
	}
	
	if(xyarray->size() < 2){
		xyarray->resize(2);
	}
	for(int j = 0; j < 2; j++){
		if((*xyarray)[j].size() < mesh[j]){
			(*xyarray)[j].resize(mesh[j]);
		}
		for(int n = 0; n < mesh[j]; n++){
			(*xyarray)[j][n] = xyini[j]+(double)n*dxy[j];
	        if(fabs((*xyarray)[j][n]) < dxy[j]*DXY_LOWER_LIMIT){
		        (*xyarray)[j][n] = 0.0;
			}
		}
	}
	
	if(fluxdens != nullptr){
		if(skipalloc == false){
			m_wigner->AllocateSpatialProfile(
				m_wigner->GetProcessLayer()-1, true, m_gtrange, m_esigma, m_dqduv, m_coefExy, 
				fluxdens, nullptr, rank, mpiprocesses, duv, ExFnearp, EyFnearp);
		}
		else if(ExFnearp != nullptr){
			m_wigner->LoadSpatialProfile(fluxdens, m_esigma, duv, ExFnearp, EyFnearp);
		}
		m_wigner->GetWignerPhaseSpaceFnear(type, 
			UVfix, uvfix, uvini, uvfin, mesh, 
			W, fluxdens, rank, mpiprocesses, netgt, ExFnearp, EyFnearp);
	}
	else{
		m_wigner->GetWignerPhaseSpace(type, 
			UVfix, uvfix, uvini, uvfin, mesh, W, fluxdens, rank, mpiprocesses);
	}

	double wcoef = m_coefWDF*m_dqduv*m_dqduv;
	if(type == WignerFuncType2DX || type == WignerFuncType2DY){
		wcoef *= (m_dqduv*1.0e+3)*(m_dXYdUV*1.0e+3);
			// m -> mm, rad -> mrad
	}
	for(int n = 0; n < mesh[0]; n++){
		(*W)[n] *= wcoef;
	}
}

void SourceCharacterization::GetSourceSize(double angle[], double size[], int rank, int mpiprocesses)
{
	double fixpoint[NumberWignerUVPrm];
	double rangeini[NumberWignerUVPrm];
	double rangefin[NumberWignerUVPrm];
	double sigmaxy[2], sxr;
	double area, mean, peak, stdpeak, cutpk = 0.01;
	double rangex;
	int meshr[NumberWignerUVPrm];
	vector<vector<double>> xarray, yarray, Wx, Wy;
	vector<double> W;

	sigmaxy[0] = BMWigglerRadiation::GetDivergence(m_penergy/m_ecritical)/m_gamma;

	rangex = min(5.0, max(1.0, (sigmaxy[0]*6.0)/(m_conf[horizacc_]*1.0e-3)));
	
	//  vertical source size
	sigmaxy[0] = wave_length(m_penergy)/4.0/PI/sigmaxy[0];
	sigmaxy[1] = sqrt(hypotsq(sigmaxy[0], m_sigmaxy[1]));

	//  horizontal source size
	sxr = max(wave_length(m_penergy)/4.0/PI/(0.5*m_conf[horizacc_]*1.0e-3), sigmaxy[0]);
	sigmaxy[0] = sqrt(hypotsq(max(m_dUmin*m_dXYdUV, m_sigmaxy[0]), sxr));

	for(int j = 0; j < NumberWignerUVPrm; j++){
		fixpoint[j] = rangeini[j] = rangefin[j] = 0;
		meshr[j] = 1;
	}
	fixpoint[WignerUVPrmu] = angle[0];
	fixpoint[WignerUVPrmv] = angle[1];
	rangefin[WignerUVPrmU] = sigmaxy[0]*m_gaussian_limit*rangex;
	if(m_iswiggler){
		rangefin[WignerUVPrmU] += m_Kxy[1][1]*m_lu/PI2/m_gamma+angle[0]*m_N*m_lu/2.0;
	}
	rangeini[WignerUVPrmU] = -rangefin[WignerUVPrmU];

	rangefin[WignerUVPrmV] = sigmaxy[1]*m_gaussian_limit;
	if(m_iswiggler){
		rangefin[WignerUVPrmV] += angle[1]*m_N*m_lu/2.0;
	}
	rangeini[WignerUVPrmV] = -rangefin[WignerUVPrmV];
	meshr[WignerUVPrmU] = (int)ceil(rangefin[WignerUVPrmU]/(sigmaxy[0]/10.0/(double)m_acclevel))*2+1;
	meshr[WignerUVPrmV] = (int)ceil(rangefin[WignerUVPrmV]/(sigmaxy[1]/10.0/(double)m_acclevel))*2+1;

	m_wigner->SetIrpt(true);
	GetPhaseSpaceProfile(WignerFuncType2DX, fixpoint, rangeini, rangefin, meshr, &xarray, &Wx, nullptr, rank, mpiprocesses);
	W.resize(xarray[0].size());
	for(int n = 0; n < xarray[0].size(); n++){
		W[n] = Wx[n][0];
	}
	FunctionStatistics fstat(xarray[0].size(), &xarray[0], &W);
	fstat.GetStatistics(&area, &mean, &peak, &size[0], &stdpeak, cutpk);

	GetPhaseSpaceProfile(WignerFuncType2DY, fixpoint, rangeini, rangefin, meshr, &yarray, &Wy, nullptr, rank, mpiprocesses, true);
	m_wigner->SetIrpt(false);
	W.resize(yarray[0].size());
	for(int n = 0; n < yarray[0].size(); n++){
		W[n] = Wy[n][0];
	}
	fstat.AssignFunction(yarray[0].size(), &yarray[0], &W);
	fstat.GetStatistics(&area, &mean, &peak, &size[1], &stdpeak, cutpk);
}

void SourceCharacterization::GetSrcProfile(double XYini[], double XYfin[], int mesh[],
		vector<vector<double>> *xyarray, vector<vector<double>> *W, FluxDensity *fluxdens, int rank, int mpiprocesses)
{
	double UVini[2], UVfin[2], dxy;
	for(int j = 0; j < 2; j++){
		UVini[j] = XYini[j]/m_dXYdUV;
		UVfin[j] = XYfin[j]/m_dXYdUV;
	}
	m_wigner->GetSrcProfile(m_dqduv, m_coefExy, m_gtrange, UVini, UVfin, mesh, m_esigma, W, fluxdens, rank, mpiprocesses);
	double coef = GetCoefSpatialProfile();
	for(int n = 0; n < mesh[0]; n++){
		(*W)[n] *= coef;
	}

	if(xyarray->size() < 2){
		xyarray->resize(2);
	}
	for(int j = 0; j < 2; j++){
		if((*xyarray)[j].size() < mesh[j]){
			(*xyarray)[j].resize(mesh[j]);
		}
		if(mesh[j] > 1){
			dxy = (XYfin[j]-XYini[j])/(double)(mesh[j]-1);
		}
		else{
			dxy = 0.0;
		}
		for(int n = 0; n < mesh[j]; n++){
			(*xyarray)[j][n] = XYini[j]+(double)n*dxy;
	        if(fabs((*xyarray)[j][n]) < dxy*DXY_LOWER_LIMIT){
		        (*xyarray)[j][n] = 0.0;
			}
		}
	}
}

double SourceCharacterization::GetCoefSpatialProfile()
{
	double dqdu = m_dqduv*m_dqduv;
	dqdu *= dqdu;
	double coef = (m_coefWDF*1.0e+6)*dqdu;
		// /mm^2/mrad^2/100%BW -> /mm^2/rad^2/0.1%BW
	return coef;
}

//---------- private functions
double SourceCharacterization::f_GTmaxU(double epsilon, int nh, int N, double *gt2uv, double *hDelta)
{
	*hDelta = MAXARGSINC+max(0.0, -epsilon/(1.0+epsilon/(double)(nh*N)));
	*hDelta = sqrt(*hDelta);
	*gt2uv = sqrt((double)(nh*N)/(1.0+m_K2));
	return (*hDelta)/(*gt2uv);
}

void SourceCharacterization::f_AssignEFieldUnd(double epsilon, int nh, int N)
{
	double hDelta, u, v, pk, gtxymax, gt2uv, gt, phi, coef;
	double delta[2], dinterv[2], hrange[2];
	int hmesh, mesh[2];
	vector<double> fxy(4);

	gtxymax = f_GTmaxU(epsilon, nh, N, &gt2uv, &hDelta);
	delta[0] = delta[1] = 1.0/16.0/(double)nh/(double)m_acclevel;

	hmesh = (int)ceil(gtxymax/delta[0]);
	for(int j = 0; j < 2; j++){
		delta[j] = (gtxymax/(double)hmesh)*gt2uv;
		mesh[j] = 2*hmesh+1;
	}

	pk = max(1.0, -epsilon);
	dinterv[0] = dinterv[1] = sqrt(1.0/32.0/pk/(double)m_acclevel);
	hrange[0] = hrange[1] = hDelta;


#ifdef DEBUG_SRC_CHAR
	FILE *fp = file_pointer_debug(DEBUG_BM_SOURCE_EXY_PROFILE);
#endif

	UndulatorFxyFarfield *uxyfar = new UndulatorFxyFarfield(*this);
	m_Ex.resize(2*hmesh+1);
	m_Ey.resize(2*hmesh+1);
	for(int nx = -hmesh; nx <= hmesh; nx++){
		u = (double)nx*delta[0];
		m_Ex[nx+hmesh].resize(2*hmesh+1);
		m_Ey[nx+hmesh].resize(2*hmesh+1);
		for(int ny = -hmesh; ny <= hmesh; ny++){
			v = (double)ny*delta[1];
			gt = sqrt(hypotsq(u, v))/gt2uv;
			if(gt > TINY){
				phi = atan2(v, u);
			}
			else{
				phi = 0.0;
			}
			uxyfar->SetCondition(nh, gt);
			uxyfar->GetFxy(phi, &fxy, true);
			coef = uxyfar->GetCoefFxy();
			m_Ex[nx+hmesh][ny+hmesh] = complex<double>(fxy[0], fxy[1])/coef;
			m_Ey[nx+hmesh][ny+hmesh] = complex<double>(fxy[2], fxy[3])/coef;
			// to be consistent with the definition of Fx,y
			m_Ex[nx+hmesh][ny+hmesh] *= m_coefExy;
			m_Ey[nx+hmesh][ny+hmesh] *= m_coefExy;
#ifdef DEBUG_SRC_CHAR
			fprintf(fp, "%g\t%g\t%g\t%g\t%g\t%g\n", u, v, 
				m_Ex[nx+hmesh][ny+hmesh].real(), m_Ex[nx+hmesh][ny+hmesh].imag(),
				m_Ey[nx+hmesh][ny+hmesh].real(), m_Ey[nx+hmesh][ny+hmesh].imag());
#endif
		}
	}
#ifdef DEBUG_SRC_CHAR
	fclose(fp);
#endif

	delete uxyfar;

	m_wigner->AssignData(&m_Ex, &m_Ey, mesh, delta, 0, 0, dinterv, hrange);
	f_AssignSn(hDelta, epsilon, nh, N);
}

void SourceCharacterization::f_AssignSn(double uvmax, double epsilon, int nh, int N)
{
	int hmesh[2], meshsn[2];
	double deltasn[2];
	double wmax = max(2.0*uvmax*uvmax, MAXARGSINC);
	deltasn[0] = deltasn[1] = 1.0/8.0/(double)m_acclevel;
	hmesh[0] = (int)ceil(wmax/deltasn[0]);
	hmesh[1] = (int)ceil(MAXARGSINC/deltasn[1]);

	for(int j = 1; j <= 2; j++){
		meshsn[j] = 2*hmesh[j]+1;
	}
	m_Sn.resize(2*hmesh[0]+1);
	for(int nx = -hmesh[0]; nx <= hmesh[0]; nx++){
		m_Sn[nx+hmesh[0]].resize(2*hmesh[1]+1);
	}
	double esigma = 2.0*m_esigma; // to convert from e-energy deviation to wavelength deviation

#ifdef DEBUG_SRC_CHAR
	FILE *fp = file_pointer_debug(DEBUG_BM_SOURCE_SN_PROFILE);
#endif

	int nfft = 1;
	while(nfft < meshsn[0]) nfft <<= 1;
	
	FastFourierTransform fft(1, nfft);
	double *data, w, dw, sarg[2], dz = PI2/((double)nfft*deltasn[0]), tex;
	data = (double *)calloc(nfft, sizeof(double));
	for(int ny = -hmesh[1]; ny <= hmesh[1]; ny++){
		dw = deltasn[1]*(double)ny;

		for(int n = 0; n < nfft; n++){
			data[n] = 0.0;
		}
		for(int nx = -hmesh[0]; nx <= hmesh[0]; nx++){
			w = deltasn[0]*(double)nx;
			sarg[0] = PI*w;
			sarg[1] = PI*(w+dw);
			data[nx+nfft/2] = sinc(sarg[0])*sinc(sarg[1]);
		}
		fft.DoRealFFT(data);
	    for(int n = 0; n <= nfft/2; n++){
			tex = (double)n*dz;
			tex *= esigma;
			tex *= tex*0.5;
			if(tex > MAXIMUM_EXPONENT){
				tex = 0.0;
			}
			else{
				tex = exp(-tex);
			}
            if(n == nfft/2){
                data[1] *= tex;
            }
            else if(n == 0){
                data[0] *= tex;
            }
            else{
                data[2*n] *= tex;
                data[2*n+1] *= tex;
            }

		}
		fft.DoRealFFT(data, -1);
		for(int nx = -hmesh[0]; nx <= hmesh[0]; nx++){
			w = deltasn[0]*(double)nx;
			m_Sn[nx+hmesh[0]][ny+hmesh[1]] = data[nx+nfft/2]*2.0/(double)nfft;
#ifdef DEBUG_SRC_CHAR
			fprintf(fp, "%g\t%g\t%g\n", w, dw, m_Sn[nx+hmesh[0]][ny+hmesh[1]]);
#endif
		}
	}

#ifdef DEBUG_SRC_CHAR
	fclose(fp);
#endif

	m_wigner->AssignDataSn(&m_Sn, meshsn, deltasn, epsilon, nh, N);

	free(data);
}

void SourceCharacterization::f_AssignEFieldWiggler(double epsilon, double deltau, bool isbma)
{
	double hDelta[2], u, v, vs, fx[2], fy[2], gtxy[2], delta[2], adelta[2];
	int hmesh[2], mesh[2], ahmesh[2], amesh[2];
	vector<vector<double>> ws(4);
	vector<double> zws;

	complex<double> exy[2], I(0.0, 1.0);
	double ev2, eubcub, bsk1, bsk2, exparg, eta0, cv, eKx, eKy, aflux;

	delta[0] = PI2/4.0/deltau/deltau/(double)m_acclevel;
	delta[1] = min(0.1, PI2/4.0/deltau/sqrt(MAXARGK1312))/(double)m_acclevel;
	hDelta[0] = deltau*0.5;
	hDelta[1] = sqrt(MAXARGK1312);
	adelta[0] = adelta[1] = ANGLEINTERVAL;

	for(int j = 0; j < 2; j++){
		hmesh[j] = max(4, (int)ceil(hDelta[j]/delta[j]));
		delta[j] = hDelta[j]/(double)hmesh[j];
		mesh[j] = 2*hmesh[j]+1;
		ahmesh[j] = max(4, (int)ceil(hDelta[j]/adelta[j]));
		amesh[j] = 2*ahmesh[j]+1;
	}

	eKy = epsilon*m_Kxy[1][1];
	eKx = epsilon*m_Kxy[0][1];

#ifdef DEBUG_SRC_CHAR
	FILE *fpxy[2];
	fpxy[0] = file_pointer_debug(DEBUG_BM_SOURCE_EXY_PROFILEX);
	fpxy[1] = file_pointer_debug(DEBUG_BM_SOURCE_EXY_PROFILEY);
	vector<double> uvarr[2], Exarr[2], phixarr[2], Eyarr[2], phiyarr[2];
	for(int j = 1; j <= 2; j++){
		uvarr[j].resize(2*hmesh[j]+1);
		Exarr[j].resize(2*hmesh[j]+1);
		phixarr[j].resize(2*hmesh[j]+1);
		Eyarr[j].resize(2*hmesh[j]+1);
		phiyarr[j].resize(2*hmesh[j]+1);
	}
	FILE *fp = file_pointer_debug(DEBUG_BM_SOURCE_EXY_PROFILE);
#endif

	m_Ex.resize(2*hmesh[0]+1);
	m_Ey.resize(2*hmesh[0]+1);
	aflux = 0.0;
	for(int nx = -hmesh[0]; nx <= hmesh[0]; nx++){
		u = (double)nx*delta[0];
		gtxy[0] = u/epsilon;
		m_Ex[nx+hmesh[0]].resize(2*hmesh[1]+1);
		m_Ey[nx+hmesh[0]].resize(2*hmesh[1]+1);
		for(int ny = -hmesh[1]; ny <= hmesh[1]; ny++){
			v = (double)ny*delta[1];
			eta0 = u/eKy;
			if(fabs(eta0) >= 1.0){
				m_Ex[nx+hmesh[0]][ny+hmesh[1]] = complex<double>(0.0, 0.0);
				m_Ey[nx+hmesh[0]][ny+hmesh[1]] = complex<double>(0.0, 0.0);
			}
			else{
				cv = 1.0-eta0*eta0;
				cv = sqrt(cv);
				vs = v-eKx*cv;
				ev2 = epsilon*epsilon+vs*vs;
				eubcub = 2.0/3.0*pow(ev2, 1.5)/cv;

				exy[0] = -I*1.5/sqrt(ev2)*Bessel::K23_u(eubcub);
				exy[1] = vs*1.5/ev2*Bessel::K13_u(eubcub);
				eta0 = asin(eta0);
				exparg = eKy*(
							eta0*(epsilon*epsilon+hypotsq(u, v)+hypotsq(eKx, eKy)*0.5)
							+(eKx*eKx-eKy*eKy)*sin(2.0*eta0)/4.0
							-2.0*eKx*v*sin(eta0)+2.0*eKy*u*(cos(eta0)-1.0)
						);
				m_Ex[nx+hmesh[0]][ny+hmesh[1]] = exy[0]*exp(complex<double>(0.0, exparg));
				m_Ey[nx+hmesh[0]][ny+hmesh[1]] = exy[1]*exp(complex<double>(0.0, exparg));
			}
			m_Ex[nx+hmesh[0]][ny+hmesh[1]] *= m_coefExy;
			m_Ey[nx+hmesh[0]][ny+hmesh[1]] *= m_coefExy;
			aflux += hypotsq(m_Ex[nx+hmesh[0]][ny+hmesh[1]].real(), m_Ex[nx+hmesh[0]][ny+hmesh[1]].imag());
			aflux += hypotsq(m_Ey[nx+hmesh[0]][ny+hmesh[1]].real(), m_Ey[nx+hmesh[0]][ny+hmesh[1]].imag());

#ifdef DEBUG_SRC_CHAR
			if(nx == 0){
				uvarr[1][ny+hmesh[1]] = v;
				Exarr[1][ny+hmesh[1]] = abs(m_Ex[nx+hmesh[0]][ny+hmesh[1]]);
				Eyarr[1][ny+hmesh[1]] = abs(m_Ey[nx+hmesh[0]][ny+hmesh[1]]);
				phixarr[1][ny+hmesh[1]] = arg(m_Ex[nx+hmesh[0]][ny+hmesh[1]]);
				phiyarr[1][ny+hmesh[1]] = arg(m_Ey[nx+hmesh[0]][ny+hmesh[1]]);
			}
			if(ny == 0){
				uvarr[0][nx+hmesh[0]] = u;
				Exarr[0][nx+hmesh[0]] = abs(m_Ex[nx+hmesh[0]][ny+hmesh[1]]);
				Eyarr[0][nx+hmesh[0]] = abs(m_Ey[nx+hmesh[0]][ny+hmesh[1]]);
				phixarr[0][nx+hmesh[0]] = arg(m_Ex[nx+hmesh[0]][ny+hmesh[1]]);
				phiyarr[0][nx+hmesh[0]] = arg(m_Ey[nx+hmesh[0]][ny+hmesh[1]]);
			}
			fprintf(fp, "%g\t%g\t%g\t%g\t%g\t%g\n", u, v, 
				m_Ex[nx+hmesh[0]][ny+hmesh[1]].real(), m_Ex[nx+hmesh[0]][ny+hmesh[1]].imag(),
				m_Ey[nx+hmesh[0]][ny+hmesh[1]].real(), m_Ey[nx+hmesh[0]][ny+hmesh[1]].imag());
#endif
		}
	}
	aflux *= delta[0]*delta[1];

#ifdef DEBUG_SRC_CHAR
	fclose(fp);

	for(int j = 1; j <= 2; j++){
		fprintf(fpxy[j], "uv\tEx\tphix\tEy\tphiy\n");
		for(int n = -hmesh[j]; n < hmesh[j]; n++){
			if(phixarr[j][n+hmesh[j]+1] > phixarr[j][n+hmesh[j]]+PId2){
				for(int ni = n+1; ni <= hmesh[j]; ni++){
					phixarr[j][ni+hmesh[j]] -= PI2;
				}
			}
			else if(phixarr[j][n+hmesh[j]+1] < phixarr[j][n+hmesh[j]]-PId2){
				for(int ni = n+1; ni <= hmesh[j]; ni++){
					phixarr[j][ni+hmesh[j]] += PI2;
				}
			}
			if(phiyarr[j][n+hmesh[j]+1] > phiyarr[j][n+hmesh[j]]+PId2){
				for(int ni = n+1; ni <= hmesh[j]; ni++){
					phiyarr[j][ni+hmesh[j]] -= PI2;
				}
			}
			else if(phiyarr[j][n+hmesh[j]+1] < phiyarr[j][n+hmesh[j]]-PId2){
				for(int ni = n+1; ni <= hmesh[j]; ni++){
					phiyarr[j][ni+hmesh[j]] += PI2;
				}
			}
		}
		for(int n = -hmesh[j]; n < hmesh[j]; n++){
			fprintf(fpxy[j], "%g\t%g\t%g\t%g\t%g\n", uvarr[j][n+hmesh[j]], 
				Exarr[j][n+hmesh[j]], phixarr[j][n+hmesh[j]], Eyarr[j][n+hmesh[j]], phiyarr[j][n+hmesh[j]]);
		}
		fclose(fpxy[j]);
	}
#endif

	m_wigner->AssignData(&m_Ex, &m_Ey, mesh, delta, eKx, eKy);
	m_wigner->AssignDataAprof(aflux, amesh, adelta);
}

void SourceCharacterization::f_AssignEFieldBM(double epsilon, double deltau)
{
	double hDelta[2], uv[2], delta[2], umax;
	double Mg = (double)(2*m_acclevel);
	int hmesh[2], mesh[2];
	complex<double> exy[2], I(0.0, 1.0);

	bool iswigner = contains(m_calctype, menu::wigner);
	if(m_confb[optDx_] && iswigner){
		double A = PI2*Mg*3.0/pow(epsilon, 3.0);
		double B = pow((A+sqrt(A*A+4.0))/2.0, 1.0/3.0);
		if(contains(m_calctype, menu::XXpslice)
			|| contains(m_calctype, menu::YYpslice)
			|| contains(m_calctype, menu::XXpYYp))
		{
			umax = max(fabs(m_confv[Xprange_][0]), fabs(m_confv[Xprange_][1]))/m_dqduv;
		}
		else{
			umax = fabs(m_conf[Xpfix_])/m_dqduv;
		}
		umax = max(umax, (B-1.0/B)*epsilon);
		deltau = min(2.0*umax, deltau);
	}

	delta[0] = PI2/4.0/deltau/deltau/(double)m_acclevel;
	delta[1] = min(0.1, PI2/4.0/deltau/sqrt(MAXARGK1312))/(double)m_acclevel;
	hDelta[0] = deltau*0.5;
	hDelta[1] = sqrt(MAXARGK1312);

	for(int j = 1; j <= 2; j++){
		hmesh[j] = max(4, (int)ceil(hDelta[j]/delta[j]));
		delta[j] = hDelta[j]/(double)hmesh[j];
		mesh[j] = 2*hmesh[j]+1;
	}

#ifdef DEBUG_SRC_CHAR
	FILE *fp = file_pointer_debug(DEBUG_BM_SOURCE_EXY_PROFILE);
#endif

	m_Ex.resize(2*hmesh[0]+1);
	m_Ey.resize(2*hmesh[0]+1);
	for(int nx = -hmesh[0]; nx <= hmesh[0]; nx++){
		uv[0] = (double)nx*delta[0];
		m_Ex[nx+hmesh[0]].resize(2*hmesh[1]+1, 0.0);
		m_Ey[nx+hmesh[0]].resize(2*hmesh[1]+1, 0.0);
		for(int ny = -hmesh[1]; ny <= hmesh[1] && iswigner; ny++){
			uv[1] = (double)ny*delta[1];
			f_GetBMExyAmpDirect(epsilon, uv, 
				&m_Ex[nx+hmesh[0]][ny+hmesh[1]], &m_Ey[nx+hmesh[0]][ny+hmesh[1]]);
#ifdef DEBUG_SRC_CHAR
			if(abs(nx)%1==0){
				fprintf(fp, "%g\t%g\t%g\t%g\t%g\t%g\n", uv[0], uv[1], 
					m_Ex[nx+hmesh[0]][ny+hmesh[1]].real(), m_Ex[nx+hmesh[0]][ny+hmesh[1]].imag(),
					m_Ey[nx+hmesh[0]][ny+hmesh[1]].real(), m_Ey[nx+hmesh[0]][ny+hmesh[1]].imag());
			}
#endif
		}
	}
#ifdef DEBUG_SRC_CHAR
	fclose(fp);
#endif

	m_wigner->AssignData(&m_Ex, &m_Ey, mesh, delta, 0, 0, nullptr, nullptr, epsilon);
}

void SourceCharacterization::f_GetBMExyAmpDirect(
	double epsilon, double uv[], complex<double> *Ex, complex<double> *Ey)
{
	double ev2 = epsilon*epsilon+uv[1]*uv[1];
	double u = 2.0/3.0*pow(ev2, 1.5);
	complex<double> Lambda(0.0, uv[0]*(ev2+uv[0]*uv[0]/3.0));
	complex<double> exy[2];
	complex<double> I(0.0, 1.0);

	complex<double> phs = exp(Lambda);

	exy[0] = -I*1.5/sqrt(ev2)*Bessel::K23_u(u)*m_coefExy;
	exy[1] = uv[1]*1.5/ev2*Bessel::K13_u(u)*m_coefExy;
	*Ex = exy[0]*phs;
	*Ey = exy[1]*phs;
}

//---------- class WignerFunction ----------
WignerFunction::WignerFunction(int acclevel, int nwiggler, bool isund, bool isoddpolewig,
	PrintCalculationStatus *status, int wlayer)
{
	m_Sn = nullptr;
	m_isnegpole = false;
	m_Nwiggler = nwiggler;
	m_idealbm = false;
	m_ncomps = max(1, nwiggler);
	m_acclevel = acclevel;
	m_isund = isund;
	m_calcstatus = status;
	m_process_layer = wlayer;
	m_oddpolewig = isoddpolewig;
	m_gaussian_limit = GAUSSIAN_MAX_REGION+acclevel-1;
	AllocateMemorySimpson(2*m_ncomps, 2*m_ncomps, 3);
    if(m_calcstatus != nullptr){
        SetCalcStatusPrint(m_calcstatus);
    }
	m_irpt = 1;
	m_ws4bm = nullptr;
	m_fft4bm = nullptr;
	m_nfftbm = 0;
}

WignerFunction::~WignerFunction()
{
	if(m_ws4bm != nullptr){
		free(m_ws4bm);
	}
	if(m_fft4bm != nullptr){
		delete m_fft4bm;
	}
}

bool WignerFunction::AssignData(
	vector<vector<complex<double>>> *Ex, vector<vector<complex<double>>> *Ey,
	int mesh[], double delta[], double eKx, double eKy, double *dinterv, double *hrange, double epsilon)
{
	if(epsilon > 0){
		m_idealbm = true;
		m_epsbm = epsilon;
	}
	m_Exp = Ex;
	m_Eyp = Ey;
	for(int j = 1; j <= 2; j++){
		if(mesh[j]%2 == 0){
			return false;
		}
		m_halfmesh[j] = (mesh[j]-1)/2;
		m_delta[j] = delta[j];
		m_mesh[j] = mesh[j];
		m_valrange[j] = (double)(m_halfmesh[j]+1.0e-3)*m_delta[j];

		if(dinterv == nullptr){
			// for undulator, calc. interval should be shorter than grid size (m_delta)
			m_dinterv[j] = m_delta[j];
			m_halfrange[j] = m_halfmesh[j]*m_dinterv[j];
		}
		else{
			m_dinterv[j] = dinterv[j];
			m_halfrange[j] = hrange[j];
		}
	}
	m_srcpoint[0] = m_srcpoint[1] = 0;
	if(m_Nwiggler >= 1){
		m_eKwiggler = eKy;
		m_eKx = eKx;
		m_srcpoint[0] = -2.0*m_eKwiggler*m_eKwiggler;
	}	
	if(Ex->size() != mesh[0]){
		return false;
	}
	for(int nx = 0; nx < mesh[0]; nx++){
		if((*Ex)[nx].size() != mesh[1]){
			return false;
		}
	}
	return true;
}

bool WignerFunction::AssignDataSn(
		vector<vector<double>> *Sn, int mesh[], double delta[], double epsilon, int nh, int N)
{
	m_Uepsilon = epsilon;
	m_Sn = Sn;
	m_Nnh = nh*N;
	for(int j = 1; j <= 2; j++){
		if(mesh[j]%2 == 0){
			return false;
		}
		m_halfmeshsn[j] = (mesh[j]-1)/2;
		m_deltasn[j] = delta[j];
		m_snmesh[j] = mesh[j];
		m_valrangesn[j] = (double)(m_halfmeshsn[j]+1.0e-3)*m_deltasn[j];
	}
	if(Sn->size() != mesh[0]){
		return false;
	}
	for(int nx = 0; nx < mesh[0]; nx++){
		if((*Sn)[nx].size() != mesh[1]){
			return false;
		}
	}
	return true;
}

bool WignerFunction::AssignDataAprof(double aflux, int mesh[], double delta[])
{
	m_aflux = aflux;
	for(int j = 1; j <= 2; j++){
		if(mesh[j]%2 == 0){
			return false;
		}
		m_adelta[j] = delta[j];
		m_amesh[j] = mesh[j];
	}
	return true;
}

bool WignerFunction::SpatialProfileSingleConv(
	int nc, vector<vector<double>> *we, vector<vector<double>> *wf)
	// spatial profile given by (angular profile) * (distance to the center (from the target period))
{
	double adxy[2]; // interval for angular-spatial profile
	double aDxy[2]; // range for angular-spatial profile
	double hDxy[2]; // half spatial range of source profile
	double hdxy[2]; // interval for source profile
	double uv[2];
	double dUVduv; // conversion from u,v to U,V (normalized distance from the wiggler center)
	double dl[2];
	double coef;
	complex<double> ewx, ewy;

	dUVduv = fabs(f_GetOmegaWiggler(nc));
	for(int j = 1; j <= 2; j++){
		adxy[j] = m_adelta[j]*dUVduv;
		aDxy[j] = adxy[j]*m_amesh[j];
		hdxy[j] = m_deltasp[j][0];
		hDxy[j] = m_deltasp[j][0]*(double)max(abs(m_spefin[j]-m_halfmeshsp[j][0]), abs(m_halfmeshsp[j][0]-m_speini[j]));
	}
	dl[0] = fabs(f_GetOmegaWiggler(nc, 0.25))+TINY;
	dl[1] = fabs(f_GetOmegaWiggler(nc, -0.25))+TINY;
	dl[0] = max(dl[0]/dl[1], dl[1]/dl[0]);
	if(adxy[0] < hdxy[0]*3.0 || adxy[1] < hdxy[1]*3.0 || dl[0] > SQRT2){
		return false;
	}

	for(int j = 1; j <= 2; j++){
		m_spmesh[j][nc] = m_amesh[j];
		m_deltasp[j][nc] = adxy[j];
		m_halfmeshsp[j][nc] = (m_spmesh[j][nc]-1)/2;
		m_valrangesp[j][nc] = m_deltasp[j][nc]*(double)m_halfmeshsp[j][nc];
	}

	coef = m_sflux/m_aflux/dUVduv/dUVduv;
	if(we->size() < m_spmesh[0][nc]){
		we->resize(m_spmesh[0][nc]);
	}
	if(wf != nullptr){
		if(wf->size() < m_spmesh[0][nc]){
			wf->resize(m_spmesh[0][nc]);
		}
	}
#ifdef DEBUG_SRC_CHAR_A
	FILE *fp = file_pointer_debug(DEBUG_EXPANDED_APROFILE);
#endif
	for(int nx = 0; nx < m_spmesh[0][nc]; nx++){
		if((*we)[nx].size() < m_spmesh[1][nc]){
			(*we)[nx].resize(m_spmesh[1][nc]);
		}
		if(wf != nullptr){
			if((*wf)[nx].size() < m_spmesh[1][nc]){
				(*wf)[nx].resize(m_spmesh[1][nc]);
			}
		}
		uv[0] = (double)(nx-m_halfmeshsp[0][nc])*m_deltasp[0][nc]/dUVduv;
		for(int ny = 0; ny < m_spmesh[1][nc]; ny++){
			uv[1] = (double)(ny-m_halfmeshsp[1][nc])*m_deltasp[1][nc]/dUVduv;
			GetExyAmplitude(uv, &ewx, &ewy);
			(*we)[nx][ny] = hypotsq(abs(ewx), abs(ewy))*coef;
			if(wf != nullptr){
				(*wf)[nx][ny] = (*we)[nx][ny];
			}
#ifdef DEBUG_SRC_CHAR_A
			fprintf(fp, "%g\t%g\t%g\n", uv[0]*dUVduv, uv[1]*dUVduv, (*we)[nx][ny]);
#endif
		}
	}
#ifdef DEBUG_SRC_CHAR_A
	fclose(fp);
#endif
	return true;
}

void WignerFunction::SpatialProfileSingle(
	int nc, vector<vector<double>> *ws, vector<vector<double>> *wa, 
	double d_eta, bool isalloc, double *duvmin)
{
	double duv[2], omega, dUV[2], uv[2], dix, phi;
	complex<double> ew, ed, ea, ewx, ewy, phs;
	vector<double *> xdata, ydata;
	bool isamp = wa != nullptr;

	if(m_Nwiggler > 0){
		omega = f_GetOmegaWiggler(nc);
	}

	for(int j = 1; j <= 2; j++){
		if(m_Nwiggler > 0){
			duv[j] = min(m_dinterv[j], PId2/(TINY+fabs(omega))/m_halfrange[j]);
		}
		else{
			duv[j] = m_dinterv[j];
		}
		if(!isalloc){
			dUV[j] = PI2/(duv[j]*(double)m_nfft[j]);
		}
	}

	for(int j = 1; j <= 2 && isalloc; j++){
		m_nfft[j] = 1;
		while(duv[j]*(double)m_nfft[j] < 2.0*m_halfrange[j]*(double)max(1, m_acclevel/4)){
			m_nfft[j] <<= 1;
		}
		dUV[j] = PI2/(duv[j]*(double)m_nfft[j]);
		if(duvmin != nullptr){
			while(dUV[j] > duvmin[j]){
				m_nfft[j] <<= 1;
				dUV[j] = PI2/(duv[j]*(double)m_nfft[j]);
			}
		}

		if(m_fft[j] != nullptr){
			delete m_fft[j];
		}
		m_fft[j] = new FastFourierTransform(1, m_nfft[j]);

		if(m_wsdata[j] != nullptr){
			free(m_wsdata[j]);
		}
		if(m_wadata[j] != nullptr){
			free(m_wadata[j]);
		}
		m_wsdata[j] = (double *)malloc(sizeof(double)*m_nfft[j]*2);
		m_wadata[j] = (double *)malloc(sizeof(double)*m_nfft[j]*2);

		if(m_Nwiggler > 0 || isamp){
			uv[3-j] = 0;
			double ewmax = 0;
			bool isex;
			for(int n = 0; n < m_nfft[j]; n++){
				int ixy = fft_index(n, m_nfft[j], 1);
				uv[j] = (double)ixy*duv[j];
				GetExyAmplitude(uv, &ewx, &ewy);
				phi = -omega*uv[j]*uv[j]*0.5;
				phs = complex<double>(cos(phi), sin(phi));
				ewx *= phs;
				ewy *= phs;
				if(m_isund){
					double uv2 = uv[j]*uv[j];
					double snarg = uv2+(m_Uepsilon-2.0*d_eta)*(1.0+uv2/(double)m_Nnh);
					ewx *= sinc(PI*snarg);
					ewy *= sinc(PI*snarg);
				}
				m_wsdata[j][2*n] = ewx.real();
				m_wsdata[j][2*n+1] = ewx.imag();
				if(ewmax < abs(ewx)){
					ewmax = abs(ewx);
					isex = true;
				}

				m_wadata[j][2*n] = ewy.real();
				m_wadata[j][2*n+1] = ewy.imag();
				if(ewmax < abs(ewy)){
					ewmax = abs(ewy);
					isex = false;
				}
			}
			if(isex){
				m_fft[j]->DoFFT(m_wsdata[j]);
				m_nskip[j] = f_GetSkipNumber(m_wsdata[j], m_nfft[j], isamp);
			}
			else{
				m_fft[j]->DoFFT(m_wadata[j]);
				m_nskip[j] = f_GetSkipNumber(m_wadata[j], m_nfft[j], isamp);
			}
		}
		else{
			m_nskip[j] = 1;
		}
		m_deltasp[j][nc] = dUV[j]*m_nskip[j];
		m_halfmeshsp[j][nc] = m_nfft[j]/2/m_nskip[j];
		m_spmesh[j][nc] = 2*m_halfmeshsp[j][nc]+1;
		m_valrangesp[j][nc] = m_deltasp[j][nc]*(double)m_halfmeshsp[j][nc];
	}

	xdata.resize(m_spmesh[0][nc]);
	ydata.resize(m_spmesh[0][nc]);
	for(int nx = 0; nx < m_spmesh[0][nc]; nx++){
		xdata[nx] = (double *)malloc(sizeof(double)*m_nfft[1]*2);
		ydata[nx] = (double *)malloc(sizeof(double)*m_nfft[1]*2);
	}

	m_calcstatus->SetSubstepNumber(m_process_layer+2, m_nfft[1]+m_spmesh[0][nc]);
	m_calcstatus->PutSteps(m_process_layer+2, 0);

	bool nonzero = false;
	for(int ny = 0; ny < m_nfft[1]; ny++){
		int iy = fft_index(ny, m_nfft[1], 1);
		uv[1] = (double)iy*duv[1];
		for(int nx = 0; nx < m_nfft[0]; nx++){
			int ix = fft_index(nx, m_nfft[0], 1);
			uv[0] = (double)ix*duv[0];
			if(fabs(uv[0]) >= m_valrange[0] || fabs(uv[1]) >= m_valrange[1]){
				m_wsdata[0][2*nx] = m_wsdata[0][2*nx+1] = m_wadata[0][2*nx] = m_wadata[0][2*nx+1] = 0.0;
				continue;
			}
			GetExyAmplitude(uv, &ewx, &ewy);
			if(m_Nwiggler > 0 || isamp){
				phi = -omega*uv[0]*uv[0]*0.5;
				phs = complex<double>(cos(phi), sin(phi));
				ewx *= phs;
				ewy *= phs;
			}
			if(m_isund){
				double uv2 = hypotsq(uv[0], uv[1]);
				double snarg = uv2+(m_Uepsilon-2.0*d_eta)*(1.0+uv2/(double)m_Nnh);
				ewx *= sinc(PI*snarg);
				ewy *= sinc(PI*snarg);
			}
			m_wsdata[0][2*nx] = ewx.real();
			m_wsdata[0][2*nx+1] = ewx.imag();
			m_wadata[0][2*nx] = ewy.real();
			m_wadata[0][2*nx+1] = ewy.imag();
			nonzero = true;
		}

		if(nonzero){
			m_fft[0]->DoFFT(m_wsdata[0]);
			m_fft[0]->DoFFT(m_wadata[0]);
		}

		for(int nxc = -m_halfmeshsp[0][nc]; nxc <= m_halfmeshsp[0][nc]; nxc++){
			int ix = fft_index(nxc*m_nskip[0], m_nfft[0], -1);
			int idx = nxc+m_halfmeshsp[0][nc];
			xdata[idx][2*ny] = m_wsdata[0][2*ix]*duv[0];
			xdata[idx][2*ny+1] = m_wsdata[0][2*ix+1]*duv[0];
			ydata[idx][2*ny] = m_wadata[0][2*ix]*duv[0];
			ydata[idx][2*ny+1] = m_wadata[0][2*ix+1]*duv[0];
		}
		m_calcstatus->AdvanceStep(m_process_layer+2);
	}

#ifdef DEBUG_SRC_CHAR_A
	FILE *fpr = file_pointer_debug(DEBUG_SPATIAL_APROFILE_WDF_FFT);
	for(int ny = -m_nfft[1]/2; ny <= m_nfft[1]/2; ny += m_nskip[1]){
		int iy = fft_index(ny, m_nfft[1], -1);
		uv[1] = (double)ny*duv[1];
		for(int nxc = -m_halfmeshsp[0][nc]; nxc <= m_halfmeshsp[0][nc]; nxc++){
			int idx = nxc+m_halfmeshsp[0][nc];
			fprintf(fpr, "%g\t%g\t%g\t%g\t%g\t%g\t%g\t%g\n", 
				(double)nxc*duv[0], uv[1], 
				xdata[idx][2*iy], xdata[idx][2*iy+1], hypotsq(xdata[idx][2*iy], xdata[idx][2*iy+1]),
				ydata[idx][2*iy], ydata[idx][2*iy+1], hypotsq(ydata[idx][2*iy], ydata[idx][2*iy+1]));
		}
	}
	fclose(fpr);
#endif

	if(ws->size() < m_spmesh[0][nc]){
		ws->resize(m_spmesh[0][nc]);
	}
	if(isamp){
		if(wa->size() < m_spmesh[0][nc]){
			wa->resize(m_spmesh[0][nc]);
		}
	}
	int mesh2 = m_spmesh[1][nc]*(isamp?2:1);
	for(int nx = 0; nx < m_spmesh[0][nc]; nx++){
		if((*ws)[nx].size() < mesh2){
			(*ws)[nx].resize(mesh2);
		}
		if(isamp){
			if((*wa)[nx].size() < mesh2){
				(*wa)[nx].resize(mesh2);
			}
		}
	}

	if(nc == 0){
		m_sflux = 0.0;
	}
	for(int nxc = -m_halfmeshsp[0][nc]; nxc <= m_halfmeshsp[0][nc]; nxc++){
		int idx = nxc+m_halfmeshsp[0][nc];
		for(int ny = 0; ny < m_nfft[1]; ny++){
			int iy = fft_index(ny, m_nfft[1], 1);
			if(m_Nwiggler > 0 || isamp){
				uv[1] = (double)iy*duv[1];
				phi = -omega*uv[1]*uv[1]*0.5;
				phs = complex<double>(cos(phi), sin(phi));

				ew = complex<double>(xdata[idx][2*ny], xdata[idx][2*ny+1])*phs;
				m_wsdata[1][2*ny] = ew.real();
				m_wsdata[1][2*ny+1] = ew.imag();

				ew = complex<double>(ydata[idx][2*ny], ydata[idx][2*ny+1])*phs;
				m_wadata[1][2*ny] = ew.real();
				m_wadata[1][2*ny+1] = ew.imag();
			}
			else{
				m_wsdata[1][2*ny] = xdata[idx][2*ny];
				m_wsdata[1][2*ny+1] = xdata[idx][2*ny+1];
				m_wadata[1][2*ny] = ydata[idx][2*ny];
				m_wadata[1][2*ny+1] = ydata[idx][2*ny+1];
			}
		}
		m_fft[1]->DoFFT(m_wsdata[1]);
		m_fft[1]->DoFFT(m_wadata[1]);
		for(int nyc = -m_halfmeshsp[1][nc]; nyc <= m_halfmeshsp[1][nc]; nyc++){
			int iy = fft_index(nyc*m_nskip[1], m_nfft[1], -1);
			int idy = nyc+m_halfmeshsp[1][nc];
			if(isamp){
				(*ws)[idx][2*idy] = m_wsdata[1][2*iy]*duv[1];
				(*ws)[idx][2*idy+1] = m_wsdata[1][2*iy+1]*duv[1];
				(*wa)[idx][2*idy] = m_wadata[1][2*iy]*duv[1];
				(*wa)[idx][2*idy+1] = m_wadata[1][2*iy+1]*duv[1];
			}
			else{
				(*ws)[idx][idy] = 
					hypotsq(m_wsdata[1][2*iy]*duv[1], m_wsdata[1][2*iy+1]*duv[1])+
					hypotsq(m_wadata[1][2*iy]*duv[1], m_wadata[1][2*iy+1]*duv[1]);
			}
			if(nc == 0){
				m_sflux += (*ws)[idx][idy];
			}	
		}
		m_calcstatus->AdvanceStep(m_process_layer+2);
	}
	if(nc == 0){
		m_sflux *= m_deltasp[0][0]*m_deltasp[1][0];
	}

	for(int nx = 0; nx < m_spmesh[0][nc]; nx++){
		free(xdata[nx]);
		free(ydata[nx]);
	}

#ifdef DEBUG_SRC_CHAR_A
	FILE *fp = file_pointer_debug(DEBUG_SPATIAL_APROFILE_WDF);
	for(int nx = -m_halfmeshsp[0][nc]; nx <= m_halfmeshsp[0][nc]; nx++){
		for(int ny = -m_halfmeshsp[1][nc]; ny <= m_halfmeshsp[1][nc]; ny+=16){
			int ixx = nx+m_halfmeshsp[0][nc];
			int iyy = ny+m_halfmeshsp[1][nc];
			if(isamp){
				fprintf(fp, "%g\t%g\t%g\t%g\t%g\t%g\t%g\t%g\n", 
					nx*m_deltasp[0][nc], ny*m_deltasp[1][nc], 
					(*ws)[ixx][2*iyy], (*ws)[ixx][2*iyy+1], hypotsq((*ws)[ixx][2*iyy], (*ws)[ixx][2*iyy+1]),
					(*wa)[ixx][2*iyy], (*wa)[ixx][2*iyy+1], hypotsq((*wa)[ixx][2*iyy], (*wa)[ixx][2*iyy+1]));
			}
			else{
				fprintf(fp, "%g\t%g\t%g\n", 
					nx*m_deltasp[1][nc], ny*m_deltasp[1][nc], (*ws)[ixx][iyy]);
			}
		}
	}
	fclose(fp);
#endif
}

void WignerFunction::LoadSpatialProfile(FluxDensity *fluxdens,
	double espread, double duv[],
	vector<vector<vector<complex<double>>>> *ExFnearp,
	vector<vector<vector<complex<double>>>> *EyFnearp)
{
	int mesh[2];

    m_nepoints = fluxdens->GetEnergyArray(&m_earray);
	f_ConfigMesh();
	mesh[0] = (*ExFnearp)[0].size();
	mesh[1] = (*ExFnearp)[0][0].size();
	m_espreadloc = espread;
	AssignData(&(*ExFnearp)[0], &(*EyFnearp)[0], mesh, duv);
}

bool WignerFunction::AllocateSpatialProfile(int layer, bool iscamp,
	double gtrange[], double espread, double dqduv, double coefEwxy, 
	FluxDensity *fluxdens, double *dUVmin,
	int rank, int mpiprocesses, double *duv,
	vector<vector<vector<complex<double>>>> *ExFnearp,
	vector<vector<vector<complex<double>>>> *EyFnearp)
{
	vector<complex<double>> ewxy[2];
	double emax, emaxorg, demax, demaxr;
	double epstrunc = 0.01/(double)m_acclevel;
	double epsmax = 0.1/(double)m_acclevel, epsde = 0.4/(double)m_acclevel;
	double thetaxy[2], duvl[2];
	int hmesh[2], mesh[2], jrep, nc;
    m_nepoints = fluxdens->GetEnergyArray(&m_earray);
	int np4 = m_nepoints*4;
	vector<double> values(np4+1);
	vector<vector<vector<complex<double>>>> *Exp, *Eyp;

	if(ExFnearp != nullptr && EyFnearp != nullptr){
		Exp = ExFnearp;
		Eyp = EyFnearp;
	}
	else{
		Exp = &m_ExFnear;
		Eyp = &m_EyFnear;
	}

	if(m_nepoints%2 > 0){
		nc = (m_nepoints-1)/2;
	}
	else{
		nc = m_nepoints/2-1;
	}

	for(int j = 1; j <= 2; j++){
		hmesh[j] = 4 << m_acclevel;
		jrep = 0;
		emax = TINY;
		do{
			hmesh[j] <<= 1;
			ewxy[0].resize(2*hmesh[j]+1);
			ewxy[1].resize(2*hmesh[j]+1);
			duvl[j] = gtrange[j]/(double)hmesh[j];
			if(jrep == 0){
				f_AllocateEwxyAxis(m_nepoints, nc+1, &values, false, 
					hmesh[j], duvl[j]*dqduv, j, &ewxy[0], &ewxy[1], fluxdens);
			}
			else{
				for(int n = hmesh[j]; n > 0; n--){
					ewxy[0][2*n] = ewxy[0][n];
					ewxy[1][2*n] = ewxy[1][n];
				}
			}
			f_AllocateEwxyAxis(m_nepoints, nc+1, &values, true, 
				hmesh[j], duvl[j]*dqduv, j, &ewxy[0], &ewxy[1], fluxdens);

#ifdef DEBUG_SRC_CHAR
			FILE *fp = file_pointer_debug(DEBUG_EWXY_PROFILE);
			for(int n = 0; n <= 2*hmesh[j]; n++){
				fprintf(fp, "%g\t%g\t%g\t%g\t%g\n", 
					(n-hmesh[j])*duvl[j]*dqduv, ewxy[0][n].real(), 
					ewxy[0][n].imag(), ewxy[1][n].real(), ewxy[1][n].imag());
			}
			fclose(fp);
#endif

			emaxorg = emax;
			emax = TINY;
			demax = 0;
			for(int n = 0; n <= 2*hmesh[j]; n++){
				emax = max(emax, sqrt(hypotsq(abs(ewxy[0][n]), abs(ewxy[1][n]))));
				if(n >= 1){
					demaxr = max(
						max(fabs(ewxy[0][n].real()-ewxy[0][n-1].real()), 
							fabs(ewxy[0][n].imag()-ewxy[0][n-1].imag())),
						max(fabs(ewxy[1][n].real()-ewxy[1][n-1].real()), 
							fabs(ewxy[1][n].imag()-ewxy[1][n-1].imag())));

					if(demaxr > demax){
						jrep+=0;
					}

					demax = max(demax, demaxr);
				}
			}
			jrep++;
		}while(fabs(emaxorg-emax)/emax > epsmax || demax/emax > epsde);

		if(iscamp == false){
			int htr = 0;
			do{
				htr++;
				demax = max(sqrt(hypotsq(abs(ewxy[0][hmesh[j]-htr]), 
								abs(ewxy[1][hmesh[j]-htr]))), 
							sqrt(hypotsq(abs(ewxy[0][hmesh[j]+htr]), 
								abs(ewxy[1][hmesh[j]+htr]))));
			}while(demax/emax > epstrunc && htr < hmesh[j]);
			hmesh[j] = htr;
		}
		mesh[j] = 2*hmesh[j]+1;
	}

	vector<vector<double>> ws, wsc;
	Exp->resize(m_nepoints);
	Eyp->resize(m_nepoints);

	try{
		for(int n = 0; n < m_nepoints; n++){
			(*Exp)[n].resize(2*hmesh[0]+1);
			(*Eyp)[n].resize(2*hmesh[0]+1);
			for(int nx = 0; nx <= 2*hmesh[0]; nx++){
				(*Exp)[n][nx].resize(2*hmesh[1]+1);
				(*Eyp)[n][nx].resize(2*hmesh[1]+1);
			}
		}
	}
	catch (...){
		return false;
	}

	f_ConfigMesh();

	vector<int> mpisteps, mpiinistep, mpifinstep;
	MPI_Status mpistatus;

	mpi_steps(1, m_nepoints, mpiprocesses, &mpisteps, &mpiinistep, &mpifinstep);
	int nesteps = mpisteps[0];
	mpi_steps(1, 2*hmesh[1]+1, mpiprocesses, &mpisteps, &mpiinistep, &mpifinstep);
	double *wsmpi, *wtmpi;
	if(mpiprocesses > 1){
		wsmpi = (double *)calloc((2*hmesh[1]+1)*np4, sizeof(double));
	}

	m_calcstatus->SetSubstepNumber(layer, 2*hmesh[0]+1+(iscamp?m_nepoints:nesteps));
	for(int nx = 0; nx <= 2*hmesh[0]; nx++){
		thetaxy[0] = (double)(nx-hmesh[0])*duvl[0]*dqduv;
		for(int ny = 0; ny <= 2*hmesh[1]; ny++){
			thetaxy[1] = (double)(ny-hmesh[1])*duvl[1]*dqduv;
			if(ny < mpiinistep[rank] || ny > mpifinstep[rank]){
				continue;
			}
			fluxdens->GetFluxItemsAt(thetaxy, &values, true);
			if(mpiprocesses > 1){
				for(int jj = 0; jj < 4; jj++){
					for(int n = 0; n < m_nepoints; n++){
						wsmpi[ny*np4+jj*m_nepoints+n] = values[n+1+jj*m_nepoints];
					}
				}
			}
			else{
				for(int n = 0; n < m_nepoints; n++){
					(*Exp)[n][nx][ny] = complex<double>(values[n+1], values[n+1+m_nepoints])*coefEwxy;
					(*Eyp)[n][nx][ny] = complex<double>(values[n+1+2*m_nepoints], values[n+1+3*m_nepoints])*coefEwxy;
				}
			}
		}
		if(mpiprocesses > 1){
			for(int k = 1; k < mpiprocesses; k++){
				if(rank == 0){
					MPI_Recv(wsmpi+mpiinistep[k]*np4, mpisteps[k]*np4, MPI_DOUBLE, k, 0, MPI_COMM_WORLD, &mpistatus);
				}
				else if(rank == k){
					MPI_Send(wsmpi+mpiinistep[k]*np4, mpisteps[k]*np4, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
				}
				MPI_Barrier(MPI_COMM_WORLD);
			}
			MPI_Bcast(wsmpi, (2*hmesh[1]+1)*np4, MPI_DOUBLE, 0, MPI_COMM_WORLD);
			for(int ny = 0; ny <= 2*hmesh[1]; ny++){
				for(int n = 0; n < m_nepoints; n++){
					(*Exp)[n][nx][ny] = complex<double>(wsmpi[ny*np4+n], wsmpi[ny*np4+n+m_nepoints])*coefEwxy;
					(*Eyp)[n][nx][ny] = complex<double>(wsmpi[ny*np4+n+2*m_nepoints], wsmpi[ny*np4+n+3*m_nepoints])*coefEwxy;
				}
			}
		}
		m_calcstatus->AdvanceStep(layer);
	}

	if(mpiprocesses > 1){
		free(wsmpi);
	}

	if(duv != nullptr){
		duv[0] = duvl[0];
		duv[1] = duvl[1];
	}

	if(iscamp){
		m_espreadloc = espread;
		return AssignData(&(*Exp)[0], &(*Eyp)[0], mesh, duvl);
	}

	double efix = fluxdens->GetFixedEnergy();
	double esigma = efix*2.0*espread;
	double es[2], derrfunc, de;

	if(m_nepoints > 1){
		de = m_earray[1]-m_earray[0];
	}

	AssignData(&(*Exp)[nc], &(*Eyp)[nc], mesh, duvl);
	SpatialProfileSingle(1, &wsc, nullptr, 0, true, dUVmin);
	m_e[0].resize(m_spmesh[0][0]);
	for(int nx = 0; nx < m_spmesh[0][0]; nx++){
		m_e[0][nx].resize(m_spmesh[1][0], 0.0);
	}

	if(mpiprocesses > 1){
		wsmpi = (double *)calloc(m_spmesh[0][0]*m_spmesh[1][0], sizeof(double));
		wtmpi = (double *)calloc(m_spmesh[0][0]*m_spmesh[1][0], sizeof(double));
	}
	mpi_steps(1, m_nepoints, mpiprocesses, &mpisteps, &mpiinistep, &mpifinstep);

	for(int n = 0; n < m_nepoints; n++){
		if(n < mpiinistep[rank] || n > mpifinstep[rank]){
			continue;
		}
		if(m_nepoints == 1){
			derrfunc = 1.0;
		}
		else{
			es[0] = (m_earray[n+1]-de*0.5-efix)/SQRT2/esigma;
			es[1] = (m_earray[n+1]+de*0.5-efix)/SQRT2/esigma;
			derrfunc = 0.5*(errf(es[1])-errf(es[0]));
		}
		m_Exp = &(*Exp)[n];
		m_Eyp = &(*Eyp)[n];
		if(n == nc){
			ws = wsc;
		}
		else{
			SpatialProfileSingle(1, &ws, nullptr, 0, false);
		}
		if(mpiprocesses > 1){
			int npp = 0;
			for(int nx = 0; nx < m_spmesh[0][0]; nx++){
				for(int ny = 0; ny < m_spmesh[1][0]; ny++){
					wsmpi[npp] += ws[nx][ny]*derrfunc;
					npp++;
				}
			}
		}
		else{
			for(int nx = 0; nx < m_spmesh[0][0]; nx++){
				for(int ny = 0; ny < m_spmesh[1][0]; ny++){
					m_e[0][nx][ny] += ws[nx][ny]*derrfunc;
				}
			}
		}
		m_calcstatus->AdvanceStep(layer);
	}
	if(mpiprocesses > 1){
		MPI_Barrier(MPI_COMM_WORLD);
		MPI_Allreduce(wsmpi, wtmpi, m_spmesh[0][0]*m_spmesh[1][0], MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
		int npp = 0;
		for(int nx = 0; nx < m_spmesh[0][0]; nx++){
			for(int ny = 0; ny < m_spmesh[1][0]; ny++){
				m_e[0][nx][ny] = wtmpi[npp];
				npp++;
			}
		}
		free(wsmpi);
		free(wtmpi);
	}

#ifdef DEBUG_SRC_CHAR
	FILE *fp = file_pointer_debug(DEBUG_SPATIAL_PROFILE_WDF);
	for(int nx = -m_halfmeshsp[0][0]; nx <= m_halfmeshsp[0][0]; nx++){
		for(int ny = -m_halfmeshsp[1][0]; ny <= m_halfmeshsp[1][0]; ny++){
			fprintf(fp, "%g\t%g\t%g\t%g\n", nx*m_deltasp[0][0], ny*m_deltasp[1][0], 
				m_e[0][nx+m_halfmeshsp[0][0]][ny+m_halfmeshsp[1][0]], wsc[nx+m_halfmeshsp[0][0]][ny+m_halfmeshsp[1][0]]);
		}
	}
	fclose(fp);
#endif

	return true;
}

void WignerFunction::AllocateSpatialProfile(double espread, 
		double *dUVmin, double *Umax, int rank, int mpiprocesses)
{
	for(int j = 1; j <= 2; j++){
		m_fft[j] = nullptr;
		m_wsdata[j] = nullptr;
		m_wadata[j] = nullptr;
	}

	m_e.resize(m_ncomps+1);
	if(m_oddpolewig){
		m_f.resize(m_ncomps+1);
	}
	for(int j = 1; j <= 2; j++){
		m_deltasp[j].resize(m_ncomps+1);
		m_spmesh[j].resize(m_ncomps+1);
		m_halfmeshsp[j].resize(m_ncomps+1);
		m_valrangesp[j].resize(m_ncomps+1);
	}

	vector<vector<double>> ws;

	if(m_isund){
		m_espreadloc = espread;
		double desp = min(PI2/8.0, espread/2.0)/(double)max(1, m_acclevel/4), dr, d_eta, tex;
		int nmesh = 0;
		if(desp > TINY){
			nmesh = (int)ceil(espread*m_gaussian_limit/desp);
		}
		
		m_calcstatus->SetSubstepNumber(m_process_layer+1, 2*nmesh+1);
		SpatialProfileSingle(1, &ws, nullptr, 0.0, true, dUVmin);
		m_e[0].resize(m_spmesh[0][0]);
		for(int nx = 0; nx < m_spmesh[0][0]; nx++){
			m_e[0][nx].resize(m_spmesh[1][0], 0.0);
		}
		for(int n = -nmesh; n <= nmesh; n++){
			if(nmesh == 0){
				dr = 1.0;
			}
			else if(n == -nmesh || n == nmesh){
				dr = desp/3.0;
			}
			else if((n+nmesh)%2 == 0){
				dr = 2.0*desp/3.0;
			}
			else{
				dr = 4.0*desp/3.0;
			}
			d_eta = desp*(double)n;
			if(espread > TINY){
				tex = d_eta/espread;
				tex *= tex*0.5;
				tex = exp(-tex)/SQRTPI2/espread;
			}
			else{
				tex = 1.0;
			}
			SpatialProfileSingle(1, &ws, nullptr, d_eta, false);
			for(int nx = 0; nx < m_spmesh[0][0]; nx++){
				for(int ny = 0; ny < m_spmesh[1][0]; ny++){
					m_e[0][nx][ny] += ws[nx][ny]*dr*tex;
				}
			}
			m_calcstatus->AdvanceStep(m_process_layer+1);
		}
#ifdef DEBUG_SRC_CHAR
		FILE *fp = file_pointer_debug(DEBUG_SPATIAL_PROFILE_WDF);
		for(int nx = -m_halfmeshsp[0][0]; nx <= m_halfmeshsp[0][0]; nx++){
			for(int ny = -m_halfmeshsp[1][0]; ny <= m_halfmeshsp[1][0]; ny++){
				fprintf(fp, "%g\t%g\t%g\n", nx*m_deltasp[0][0], ny*m_deltasp[1][0], 
					m_e[0][nx+m_halfmeshsp[0][0]][ny+m_halfmeshsp[1][0]]);
			}
		}
		fclose(fp);
#endif
	}
	else if(m_Nwiggler > 0){
		m_calcstatus->SetSubstepNumber(m_process_layer+1, m_ncomps*(m_oddpolewig?2:1));

		SpatialProfileSingle(0, &m_e[0], nullptr);
		f_AssignSpRange();

		vector<int> dirper;
		for(int nc = 1; nc <= m_ncomps; nc++){
			if(SpatialProfileSingleConv(nc, &m_e[nc], m_oddpolewig?&m_f[nc]:nullptr)){
				m_calcstatus->AdvanceStep(m_process_layer+1);
				continue;
			}
			dirper.push_back(nc);
		}

		vector<int> mpisteps, mpiinistep, mpifinstep;

		mpi_steps(1, dirper.size(), mpiprocesses, &mpisteps, &mpiinistep, &mpifinstep);
		for(int ppr = 0; ppr < dirper.size(); ppr++){
			if(ppr < mpiinistep[rank] || ppr > mpifinstep[rank]){
				continue;
			}
			int nc = dirper[ppr];
			SpatialProfileSingle(nc, &m_e[nc], nullptr);
			if(m_oddpolewig){
				m_isnegpole = true;
				SpatialProfileSingle(nc, &m_f[nc], nullptr);
				m_isnegpole = false;
			}
			m_calcstatus->AdvanceStep(m_process_layer+1);
		}

		if(mpiprocesses > 1){
			MPI_Barrier(MPI_COMM_WORLD);
			int meshmax = 0;
			for(int kr = 0; kr < mpiprocesses; kr++){
				for(int nd = mpiinistep[kr]; nd <= mpifinstep[kr]; nd++){
					int nc = dirper[nd];
					for(int j = 1; j <= 2; j++){
						MPI_Bcast(&m_deltasp[j][nc], 1, MPI_DOUBLE, kr, MPI_COMM_WORLD);
						MPI_Bcast(&m_halfmeshsp[j][nc], 1, MPI_INT, kr, MPI_COMM_WORLD);
						MPI_Bcast(&m_spmesh[j][nc], 1, MPI_INT, kr, MPI_COMM_WORLD);
						MPI_Bcast(&m_valrangesp[j][nc], 1, MPI_DOUBLE, kr, MPI_COMM_WORLD);
					}
					MPI_Barrier(MPI_COMM_WORLD);
					meshmax = max(meshmax, m_spmesh[0][nc]*m_spmesh[1][nc]);
					if(kr != rank){
						m_e[nc].resize(m_spmesh[0][nc]);
						if(m_oddpolewig){
							m_f[nc].resize(m_spmesh[0][nc]);
						}
						for(int nx = 0; nx < m_spmesh[0][nc]; nx++){
							m_e[nc][nx].resize(m_spmesh[1][nc]);
							if(m_oddpolewig){
								m_f[nc][nx].resize(m_spmesh[1][nc]);
							}
						}
					}
				}
			}
			double *etmp, *ftmp;
			etmp = (double *)malloc(meshmax*sizeof(double));
			if(m_oddpolewig){
				ftmp = (double *)malloc(meshmax*sizeof(double));
			}
			for(int kr = 0; kr < mpiprocesses; kr++){
				for(int nd = mpiinistep[kr]; nd <= mpifinstep[kr]; nd++){
					int nc = dirper[nd];
					if(kr == rank){
						for(int nx = 0; nx < m_spmesh[0][nc]; nx++){
							for(int ny = 0; ny < m_spmesh[1][nc]; ny++){
								etmp[nx*m_spmesh[1][nc]+ny] = m_e[nc][nx][ny];
								if(m_oddpolewig){
									ftmp[nx*m_spmesh[1][nc]+ny] = m_f[nc][nx][ny];
								}
							}
						}
					}
					MPI_Bcast(etmp, m_spmesh[0][nc]*m_spmesh[1][nc], MPI_DOUBLE, kr, MPI_COMM_WORLD);
					if(m_oddpolewig){
						MPI_Bcast(ftmp, m_spmesh[0][nc]*m_spmesh[1][nc], MPI_DOUBLE, kr, MPI_COMM_WORLD);
					}
					if(kr != rank){
						for(int nx = 0; nx < m_spmesh[0][nc]; nx++){
							for(int ny = 0; ny < m_spmesh[1][nc]; ny++){
								m_e[nc][nx][ny] = etmp[nx*m_spmesh[1][nc]+ny];
								if(m_oddpolewig){
									m_f[nc][nx][ny] = ftmp[nx*m_spmesh[1][nc]+ny];
								}
							}
						}
					}
				}
			}
			free(etmp);
			if(m_oddpolewig){
				free(ftmp);
			}
		}

	}
	else if(m_idealbm){
		double dp = 3.0*PI/16.0/(double)m_acclevel;
		m_deltasp[0][0] = dp/max(1.0, sqrt(*Umax));
		m_deltasp[1][0] = dp;
	}
	else{
		m_calcstatus->SetSubstepNumber(m_process_layer+1, m_ncomps*(m_oddpolewig?2:1));

		for(int nc = 1; nc <= m_ncomps; nc++){
			SpatialProfileSingle(nc, &m_e[nc], nullptr);
			if(m_oddpolewig){
				m_isnegpole = true;
				SpatialProfileSingle(nc, &m_f[nc], nullptr);
				m_isnegpole = false;
			}
			m_calcstatus->AdvanceStep(m_process_layer+1);
		}
	}
	f_ClearPointers();
}

void WignerFunction::AssignCondition(double sigmauv[], double sigmaUV[], double alpha[])
{
	for(int j = 1; j <= 2; j++){
		m_sigmauv[j] = sigmauv[j];
		m_sigmaUV[j] = sigmaUV[j];
		m_alpha[j] = alpha[j];
	}
}

void WignerFunction::SetIrpt(bool ison)
{
	m_irpt = ison ? 2 : 1;
}

void WignerFunction::SetEwxyPointer(int eindex)
{
	m_Exp = &m_ExFnear[eindex];
	m_Eyp = &m_EyFnear[eindex];
}

void WignerFunction::GetExyAmplitude(double xy[], complex<double> *Ex, complex<double> *Ey)
{
	int index[2];
	double dresxy[5];
	complex<double> res;

	if(!get_2d_matrix_indices(xy, m_valrange, m_delta, m_mesh, index, dresxy)){
		*Ex = *Ey = complex<double>(0.0, 0.0);
		return;
	}

	*Ex = (*m_Exp)[index[0]  ][index[1]  ]*dresxy[0]
		+ (*m_Exp)[index[0]+1][index[1]  ]*dresxy[1]
		+ (*m_Exp)[index[0]  ][index[1]+1]*dresxy[2]
		+ (*m_Exp)[index[0]+1][index[1]+1]*dresxy[3];

	*Ey = (*m_Eyp)[index[0]  ][index[1]  ]*dresxy[0]
		+ (*m_Eyp)[index[0]+1][index[1]  ]*dresxy[1]
		+ (*m_Eyp)[index[0]  ][index[1]+1]*dresxy[2]
		+ (*m_Eyp)[index[0]+1][index[1]+1]*dresxy[3];
}

double WignerFunction::GetFluxSrcPoint(double UV[])
{
	if(m_idealbm){
		double Ex = m_bmsrcfspl[0].GetValue(UV[1]);
		double Ey = m_bmsrcfspl[1].GetValue(UV[1]);
		return hypotsq(Ex, Ey);
	}

	int index[2];
	double dresxy[4];
	double res = 0;
	int nflip = m_Nwiggler > 0 ? 1 : 0;
	double UVr[2];
	double valrange[2], delta[2];
	int tmesh[2], hmesh[2];

	for(int nc = 1; nc <= m_ncomps; nc++){
		for(int j = 1; j <= 2; j++){
			valrange[j] = m_valrangesp[j][nc];
			delta[j] = m_deltasp[j][nc];
			tmesh[j] = m_halfmeshsp[j][nc]*2+1;
			hmesh[j] = m_halfmeshsp[j][nc];
		}
		for(int n = -nflip; n <= nflip; n += 2){
			if(m_oddpolewig && nc == m_ncomps && n > 0){
				continue;
			}
			for(int j = 1; j <= 2; j++){
				if(m_oddpolewig){
					UVr[j] = UV[j]-(n < 0 ? -1.0 : 1.0)*m_srcpoint[j];
				}
				else{
					UVr[j] = (n < 0 ? -1.0 : 1.0)*UV[j]-m_srcpoint[j];
				}
			}	
			if(!get_2d_matrix_indices(UVr, valrange, delta, tmesh, index, dresxy)){
				continue;
			}
			if(m_oddpolewig && n < 0){
				res += m_f[nc][index[0]  ][index[1]  ]*dresxy[0]
					+  m_f[nc][index[0]+1][index[1]  ]*dresxy[1]
					+  m_f[nc][index[0]  ][index[1]+1]*dresxy[2]
					+  m_f[nc][index[0]+1][index[1]+1]*dresxy[3];
			}
			else{
				res += m_e[nc][index[0]  ][index[1]  ]*dresxy[0]
					+  m_e[nc][index[0]+1][index[1]  ]*dresxy[1]
					+  m_e[nc][index[0]  ][index[1]+1]*dresxy[2]
					+  m_e[nc][index[0]+1][index[1]+1]*dresxy[3];
			}
		}
	}

	return res;
}

double WignerFunction::GetSn(double u[], double v[])
{
	int index[2];
	double dresxy[5], w[2], res;

	for(int j = 1; j <= 2; j++){
		w[j] = hypotsq(u[j], v[j])*(1.0+m_Uepsilon/(double)m_Nnh)+m_Uepsilon;
	}
	w[1] -= w[0];

	if(!get_2d_matrix_indices(w, m_valrangesn, m_deltasn, m_snmesh, index, dresxy)){
		return 0.0;
	}
	res = (*m_Sn)[index[0]  ][index[1]  ]*dresxy[0]
		+ (*m_Sn)[index[0]+1][index[1]  ]*dresxy[1]
		+ (*m_Sn)[index[0]  ][index[1]+1]*dresxy[2]
		+ (*m_Sn)[index[0]+1][index[1]+1]*dresxy[3];

	return res;
}

void WignerFunction::QSimpsonIntegrand(int layer, double uv, vector<double> *W)
{
	switch(layer){
		case WignerIntegOrderU:
			f_Integrand_u(uv, W);
			break;
		case WignerIntegOrderV:
			f_Integrand_v(uv, W);
			break;
		case WignerIntegOrderUVcv:
			f_Convolute_uv(m_uvcvidx, uv, W);
			break;
	}
}

void WignerFunction::GetSrcProfile(double dqduv, double coefExy, double uvrange[],
		double UVini[], double UVfin[], int mesh[], double espread, vector<vector<double>> *W, FluxDensity *fluxdens,
		int rank, int mpiprocesses)
{
	double sigmaUV[2], dUV[2], duv[2], deltaspmin[2], dUVmin[2], Umax;
	int iskip[2], nfft[2], offset[2];

	for(int j = 1; j <= 2; j++){
		mesh[j] = max(2, mesh[j]);
		dUV[j] = (UVfin[j]-UVini[j])/(double)(mesh[j]-1);
		sigmaUV[j] = sqrt(hypotsq(m_sigmaUV[j], m_alpha[j]*m_sigmauv[j]));
		dUVmin[j] = max(fabs(dUV[j]), sigmaUV[j]);
	}
	Umax = fabs(min(UVini[0], UVfin[1]));

	W->resize(mesh[0]);
	for(int n = 0; n < mesh[0]; n++){
		(*W)[n].resize(mesh[1]);
	}

	m_calcstatus->SetTargetAccuracy(m_process_layer, 1e-3);
	m_calcstatus->SetCurrentAccuracy(m_process_layer, 2e-3);
	if(fluxdens != nullptr){
		AllocateSpatialProfile(m_process_layer+1, false, uvrange, espread, dqduv, coefExy, fluxdens, dUVmin, rank, mpiprocesses);
	}
	else{
		AllocateSpatialProfile(espread, dUVmin, &Umax, rank, mpiprocesses);
	}

	for(int j = 1; j <= 2; j++){
		deltaspmin[j] = m_deltasp[j][0];
		for(int nc = 2; nc <= m_ncomps; nc++){
			deltaspmin[j] = min(deltaspmin[j], m_deltasp[j][nc]);
		}
	}

	for(int j = 1; j <= 2; j++){
		iskip[j] = 1;
		while(dUV[j] > 2.0*deltaspmin[j]){
			iskip[j] <<= 1;
			dUV[j] /= 2.0;
		}
		nfft[j] = 1;
		double UVrange = fabs(UVfin[j]-UVini[j])+sigmaUV[j]*m_gaussian_limit*2.0; 
				// to avoid contamination by FFT convolution
		while((double)nfft[j]*dUV[j] < UVrange){
			nfft[j] <<= 1;
		}
		duv[j] = PI2/((double)nfft[j]*dUV[j]);
		if(sigmaUV[j] < TINY){
			offset[j] = 0;
		}
		else{
			offset[j] = (int)floor(sigmaUV[j]*m_gaussian_limit/dUV[j])+1;
		}
	}
	m_calcstatus->SetTargetAccuracy(m_process_layer, 1);
	m_calcstatus->SetCurrentAccuracy(m_process_layer, 1);

	FastFourierTransform *fft = new FastFourierTransform(1, nfft[1]);
	double *data  = (double *)malloc(sizeof(double)*nfft[1]);
	double **datax = (double **)malloc(sizeof(double *)*(mesh[1]));
	for(int n = 0; n < mesh[1]; n++){
		datax[n] = (double *)malloc(sizeof(double)*nfft[0]);
	}

	m_calcstatus->SetSubstepNumber(m_process_layer, mesh[1]/mpiprocesses+nfft[0]/mpiprocesses);

	double UV[2], uv, tex;

	for(int nx = rank; nx < nfft[0]; nx += mpiprocesses){
		UV[0] = (double)(nx-offset[0])*dUV[0]+UVini[0];
		if(m_idealbm){
			f_ApplyBMSourceFlux(UV[0]);
		}
		for(int ny = 0; ny < nfft[1]; ny++){
			UV[1] = (double)(ny-offset[1])*dUV[1]+UVini[1];
			data[ny] = GetFluxSrcPoint(UV);
		}
		fft->DoRealFFT(data);
		for(int ny = 0; ny <= nfft[1]/2; ny++){
			uv = ny*duv[1];
			tex = uv*sigmaUV[1];
			tex *= tex*0.5;
			if(tex > MAXIMUM_EXPONENT){
				tex = 0.0;
			}
			else{
				tex = exp(-tex)*2.0/(double)nfft[1];
			}
			if(ny == nfft[1]/2){
				data[1] *= tex;
			}
			else if(ny == 0){
				data[0] *= tex;
			}
			else{
				data[2*ny] *= tex;
				data[2*ny+1] *= tex;
			}
		}
		fft->DoRealFFT(data, -1);
		for(int ny = 0; ny < mesh[1]; ny++){
			datax[ny][nx] = data[ny*iskip[1]+offset[1]];
		}
		m_calcstatus->AdvanceStep(m_process_layer);
	}

	if(mpiprocesses > 1){
		double *wsmpi = (double *)malloc(mesh[1]*sizeof(double));
		for(int nx = 0; nx < nfft[0]; nx++){
			if(nx%mpiprocesses == rank){
				for(int ny = 0; ny < mesh[1]; ny++){
					wsmpi[ny] = datax[ny][nx];
				}
			}
			MPI_Bcast(wsmpi, mesh[1], MPI_DOUBLE, nx%mpiprocesses, MPI_COMM_WORLD);
			if(nx%mpiprocesses != rank){
				for(int ny = 0; ny < mesh[1]; ny++){
					datax[ny][nx] = wsmpi[ny];
				}
			}
		}
		free(wsmpi);
	}

	delete fft;
	fft = new FastFourierTransform(1, nfft[0]);

	for(int ny = rank; ny < mesh[1]; ny += mpiprocesses){
		fft->DoRealFFT(datax[ny]);
		for(int nx = 0; nx <= nfft[0]/2; nx++){
			uv = nx*duv[0];
			tex = uv*sigmaUV[0];
			tex *= tex*0.5;
			if(tex > MAXIMUM_EXPONENT){
				tex = 0.0;
			}
			else{
				tex = exp(-tex)*2.0/(double)nfft[0];
			}
			if(nx == nfft[0]/2){
				datax[ny][0] *= tex;
			}
			else if(nx == 0){
				datax[ny][0] *= tex;
			}
			else{
				datax[ny][2*nx] *= tex;
				datax[ny][2*nx+1] *= tex;
			}
		}
		fft->DoRealFFT(datax[ny], -1);
		for(int nx = 0; nx < mesh[0]; nx++){
			(*W)[nx][ny] = datax[ny][nx*iskip[0]+offset[0]];
		}
		m_calcstatus->AdvanceStep(m_process_layer);
	}

	if(mpiprocesses > 1){
		double *wsmpi = (double *)malloc(mesh[0]*sizeof(double));
		for(int ny = 0; ny < mesh[1]; ny++){
			if(ny%mpiprocesses == rank){
				for(int nx = 0; nx < mesh[0]; nx++){
					wsmpi[nx] = (*W)[nx][ny];
				}
			}
			MPI_Bcast(wsmpi, mesh[0], MPI_DOUBLE, ny%mpiprocesses, MPI_COMM_WORLD);
			if(ny%mpiprocesses != rank){
				for(int nx = 0; nx < mesh[0]; nx++){
					(*W)[nx][ny] = wsmpi[nx];
				}
			}
		}
		free(wsmpi);
	}


#ifdef DEBUG_SRC_CHAR
	FILE *fp = file_pointer_debug(DEBUG_WIGNER_MATRIX);
	for(int nx = 0; nx < mesh[0]; nx++){
		UV[0] = dUV[0]*(double)(iskip[0]*nx)+UVini[0];
		for(int ny = 0; ny < mesh[1]; ny++){
			UV[1] = dUV[1]*(double)(iskip[1]*ny)+UVini[1];
			fprintf(fp, "%g\t%g\t%g\n", UV[0], UV[1], (*W)[nx][ny]);
		}
	}
	fclose(fp);
#endif

	delete fft;
	free(data);
	for(int n = 0; n < mesh[1]; n++){
		free(datax[n]);
	}
	free(datax);
}

void WignerFunction::GetWignerPhaseSpaceFnear(int type, 
		double UVfix[], double uvfix[], double uvini[], double uvfin[], int mesh[],
		vector<vector<double>> *W, FluxDensity *fluxdens, int rank, int mpiprocesses, int netgt,
		vector<vector<vector<complex<double>>>> *ExFnearp,
		vector<vector<vector<complex<double>>>> *EyFnearp)
{
	vector<vector<double>> Wr;
	double derrfunc, es[2], de;
	
	if(m_nepoints > 1){
		de = m_earray[1]-m_earray[0];
	}
	double efix = fluxdens->GetFixedEnergy();
	double esigma = efix*2.0*m_espreadloc;

	if(W->size() < mesh[0]){
		W->resize(mesh[0]);
	}
	for(int i = 0; i < mesh[0]; i++){
		if((*W)[i].size() < mesh[1]){
			(*W)[i].resize(mesh[1]);
		}
		else{
			fill((*W)[i].begin(), (*W)[i].end(), 0.0);
		}
	}

	int nini, nfin;
	if(netgt < 0){
		nini = 0;
		nfin = m_nepoints-1;
	}
	else{
		nini = nfin = netgt;
	}
	for(int n = nini; n <= nfin; n++){
		if(ExFnearp != nullptr){
			m_Exp = &(*ExFnearp)[n-1];
			m_Eyp = &(*EyFnearp)[n-1];
		}
		else{
			SetEwxyPointer(n);
		}
		GetWignerPhaseSpace(type,  UVfix, uvfix, uvini, uvfin, mesh, &Wr, fluxdens, rank, mpiprocesses);
		if(m_nepoints == 1 || netgt >= 0){
			derrfunc = 1.0;
		}
		else{
			es[0] = (m_earray[n+1]-de*0.5-efix)/SQRT2/esigma;
			es[1] = (m_earray[n+1]+de*0.5-efix)/SQRT2/esigma;
			derrfunc = 0.5*(errf(es[1])-errf(es[0]));
		}
		for(int nuv = 0; nuv < mesh[0]; nuv++){
			for(int nUV = 0; nUV < mesh[1]; nUV++){
				(*W)[nuv][nUV] += Wr[nuv][nUV]*derrfunc;
			}
		}
		m_calcstatus->AdvanceStep(m_process_layer-1);

#ifdef DEBUG_SRC_CHAR
		FILE *fp = file_pointer_debug(DEBUG_WIGNER_ESPRE);
		for(int i = 0; i < mesh[0]; i++){
			for(int n = 0; n < mesh[1]; n++){
				fprintf(fp, "%d %d %g\n", i , n, Wr[i][n]);
			}
		}

		fclose(fp);
#endif
	}
}

void WignerFunction::GetWignerPhaseSpace(int type, 
		double UVfix[], double uvfix[], double uvini[], double uvfin[], int mesh[],
		vector<vector<double>> *W, FluxDensity *fluxdens, int rank, int mpiprocesses)
{
	vector<vector<double>> uvarray;

	m_type = type;
	switch(type){
		case WignerFuncType4DX:
		case WignerFuncType2DX:
		case WignerFuncType3DX:
		case WignerFuncTypeXY:
			m_uvcvidx =  2;
			m_uvscidx = 1;
			break;
		default:
			m_uvcvidx =  1;
			m_uvscidx = 2;
			break;
	}

	double duv[2];
	uvarray.resize(3);
	for(int j = 1; j <= 2; j++){
		m_uvfix[j] = uvfix[j];
		if(mesh[j] < 2){
			duv[j] = 0;
		}
		else{
			duv[j] = (uvfin[j]-uvini[j])/(double)(mesh[j]-1);
		}
		uvarray[j].resize(mesh[j]);
		for(int i = 0; i < mesh[j]; i++){
			uvarray[j][i] = uvini[j]+duv[j]*(double)i;
		}
	}

	if(W->size() < mesh[0]){
		W->resize(mesh[0]);
	}
	for(int i = 0; i < mesh[0]; i++){
		if((*W)[i].size() < mesh[1]){
			(*W)[i].resize(mesh[1]);
		}
	}

	int iscan;
	if(type == WignerFuncTypeXY){
		m_nUVpoints = mesh[1];
		m_UVpoints.resize(m_nUVpoints);
		for(int i = 0; i < mesh[1]; i++){
			m_UVpoints[i] = uvarray[1][i];
		}
		iscan = 1;
	}
	else{
		m_nUVpoints = 1;
		m_UVpoints.resize(1, UVfix[m_uvcvidx]);
		iscan = mesh[1];
	}
	AllocateMemoryFuncDigitizer(2*m_ncomps*m_nUVpoints);
	m_wsorg.resize(2*m_ncomps+1);

	m_calcstatus->SetSubstepNumber(m_process_layer, iscan*(m_Nwiggler>0?2:1)*m_irpt);

	vector<vector<double>> Wsglp, Wsglm;

	for(int iuv = 0; iuv < iscan; iuv++){
		double uv = type == WignerFuncTypeXY ? m_uvfix[0] : uvarray[1][iuv];
		f_GetWignerAlongUV(uv, &(uvarray[0]), &Wsglp, rank, mpiprocesses);
		m_calcstatus->AdvanceStep(m_process_layer);
		
		if(m_Nwiggler > 0){
			m_isnegpole = true;
			f_GetWignerAlongUV(uv, &(uvarray[0]), &Wsglm, rank, mpiprocesses);
			m_calcstatus->AdvanceStep(m_process_layer);
			m_isnegpole = false;
		}

		if(type == WignerFuncTypeXY){
			for(int iUV = 0; iUV < mesh[0]; iUV++){
				(*W)[iUV] = Wsglp[iUV];
				if(m_Nwiggler > 0){
					(*W)[iUV] += Wsglm[iUV];
				}
			}
			continue;
		}
		for(int iUV = 0; iUV < mesh[0]; iUV++){
			(*W)[iUV][iuv] = Wsglp[iUV][0];
			if(m_Nwiggler > 0){
				(*W)[iUV][iuv] += Wsglm[iUV][0];
			}
			if(type == WignerFuncType2DX || type == WignerFuncType2DY 
					|| m_type == WignerFuncType3DX || m_type == WignerFuncType3DY){
				(*W)[iUV][iuv] *=  PI2;
			}
		}
	}

#ifdef DEBUG_SRC_CHAR
	FILE *fp = file_pointer_debug(DEBUG_WIGNER_MATRIX);
	for(int iUV = 0; iUV < mesh[0]; iUV++){
		for(int iuv = 0; iuv < mesh[1]; iuv++){
			fprintf(fp, "%g\t%g\t%g\n", uvarray[0][iUV], uvarray[1][iuv], (*W)[iUV][iuv]);
		}
	}
	fclose(fp);
#endif
}

double WignerFunction::Function4Digitizer(double uv, vector<double> *W)
{
	double uvrange[2], w, wn;
	int layers[2] = {WignerIntegOrderUVcv, -1};
	vector<double> uvrangew;
	vector<double> Wsgl(3);
    vector<vector<double>> Wsum(WignerIntegOrderUVcv+1);

	double tex = uv*m_sigmaUV[m_uvscidx];
	tex *= tex*0.5;
	if(tex > MAXIMUM_EXPONENT){
		f_PutZeroValues(W, m_nUVpoints);
		return 0.0;
	}
	tex = exp(-tex);

	m_uvcv[m_uvscidx] = uv;

	if(m_type == WignerFuncType2DX || m_type == WignerFuncType2DY 
			|| m_type == WignerFuncType3DX || m_type == WignerFuncType3DY){
		QSimpsonIntegrand(WignerIntegOrderUVcv, 0.0, W);
	}
	else{
		f_GetFTRange(m_uvcvidx, uvrange);
		if(m_sigmaUV[m_uvcvidx] > TINY){
			uvrange[0] = max(uvrange[0], -m_gaussian_limit/m_sigmaUV[m_uvcvidx]);
			uvrange[1] = min(uvrange[1], m_gaussian_limit/m_sigmaUV[m_uvcvidx]);
		}

		if(uvrange[1] <= uvrange[0]){
			f_PutZeroValues(W, m_nUVpoints);
			return 0.0;
		}

		int qlevel[2];
		f_GetIntegralLevel(uvrange, m_uvcvidx, qlevel);

		IntegrateSimpson(layers, uvrange[0], uvrange[1], 0.2/(double)m_acclevel, 
			qlevel[0], nullptr, &m_wsorg, WignerIntegCUVU, false, true, qlevel[1]);
		int N = GetEvaluatedValue(WignerIntegOrderUVcv, 
				&m_wsarg[WignerIntegOrderUVcv], &m_wsval[WignerIntegOrderUVcv], WignerIntegCUVU);
		for(int np = 0; np < m_nUVpoints; np++){
			w = m_UVpoints[np]*(m_isnegpole?-1.0:1.0)-m_srcpoint[m_uvcvidx];
			if(m_Nwiggler > 0 || fabs(w*(uvrange[1]-uvrange[0])) >= MAX_ARG_SN_APPROX){
				for(int nc = 1; nc <= m_ncomps; nc++){
					if(m_Nwiggler > 0){
						wn = w-f_GetOmegaWiggler(nc)*m_uvfix[m_uvcvidx];
					}
					else{
						wn = w;
					}
					f_ReIntegrateEwit(nc, np, -wn, N,  &m_wsarg[WignerIntegOrderUVcv], &m_wsval[WignerIntegOrderUVcv], W);
				}	
			}
			else{
				for(int nc = 1; nc <= 2*m_ncomps; nc++){
					(*W)[np*2*m_ncomps+nc] = m_wsorg[nc];
				}
			}
		}
	}

	double wref = 0;
	for(int nc = 1; nc <= 2*m_ncomps*m_nUVpoints; nc++){
		(*W)[nc] *= tex;
		if(nc%2 > 0){
			wref += fabs((*W)[nc]);
		}
	}

	return wref;
}

//---------- private functions

void WignerFunction::f_ClearPointers()
{
	for(int j = 1; j <= 2; j++){
		if(m_fft[j] != nullptr){
			delete m_fft[j];
			m_fft[j] = nullptr;
		}
		if(m_wsdata[j] != nullptr){
			free(m_wsdata[j]);
			m_wsdata[j] = nullptr;
		}
		if(m_wadata[j] != nullptr){
			free(m_wadata[j]);
			m_wadata[j] = nullptr;
		}
	}
}

void WignerFunction::f_ConfigMesh()
{
	for(int j = 1; j <= 2; j++){
		m_fft[j] = nullptr;
		m_wsdata[j] = nullptr;
		m_wadata[j] = nullptr;
	}
	m_e.resize(m_ncomps+1);
	for(int j = 1; j <= 2; j++){
		m_deltasp[j].resize(m_ncomps+1);
		m_spmesh[j].resize(m_ncomps+1);
		m_halfmeshsp[j].resize(m_ncomps+1);
		m_valrangesp[j].resize(m_ncomps+1);
	}
}

void WignerFunction::f_ApplyBMSourceFlux(double U)
{
	double dv = 3.0*PI/16.0/m_acclevel, v, evv;
	double epsq = m_epsbm*m_epsbm;
	if(U+epsq < 0){
		dv /= max(2.0*m_halfrange[1], -U-epsq);
	}
	else{
		dv /= 2.0*m_halfrange[1];
	}
	int ndata = (int)ceil(m_halfrange[1]/dv);
	int nfft = 1;
	while(nfft < ndata*1.5) nfft <<= 1;
	double dV = PI2/((double)nfft*dv);

	if(m_nfftbm != nfft){
		if(m_fft4bm != nullptr){
			delete m_fft4bm;
		}
		m_fft4bm = new FastFourierTransform(1, nfft);
		m_nfftbm = nfft;
	}
	if(m_Varr4bm.size() < nfft){
		m_Varr4bm.resize(nfft);
		for(int j = 0; j < 2; j++){
			m_Earr4bm[j].resize(nfft);
		}
		m_ws4bm = (double *)realloc(m_ws4bm, sizeof(double)*nfft);
	}
	for(int n = -nfft/2; n < nfft/2; n++){
		m_Varr4bm[n+nfft/2] = dV*(double)n;
	}
	double coef = 4.0*PI*m_epsbm*dv;
	for(int j = 1; j <= 2; j++){
		for(int n = 0; n < nfft; n++){
			v = (double)fft_index(n, nfft, 1)*dv;
			evv = v*v+epsq;
			if(j == 1){
				m_ws4bm[n] = coef*Bessel::AiP(evv)*Bessel::Ai(evv+U);
			}
			else{
				m_ws4bm[n] = coef*Bessel::Ai(evv)*Bessel::Ai(evv+U)*v/sqrt(evv);
			}
		}

#ifdef DEBUG_SRC_CHAR
		FILE *fp = file_pointer_debug(DEBUG_BM_SRC_BEF);
		fprintf(fp, "v E\n");
		for(int n = 0; n < nfft; n++){
			v = (double)fft_index(n, nfft, 1)*dv;
			fprintf(fp, "%g %g\n", v, m_ws4bm[n]);
		}
		fclose(fp);
#endif
		m_fft4bm->DoRealFFT(m_ws4bm);

		if(j == 1){
			m_Earr4bm[j][nfft/2] = m_ws4bm[0];
			for(int n =  1; n < nfft/2; n++){
				m_Earr4bm[j][nfft/2-n] = m_Earr4bm[j][nfft/2+n] = m_ws4bm[2*n];
			}
			m_Earr4bm[j][0] = 0;
		}
		else{
			m_Earr4bm[j][nfft/2] = 0;
			for(int n =  1; n < nfft/2; n++){
				m_Earr4bm[j][nfft/2+n] = m_ws4bm[2*n+1];
				m_Earr4bm[j][nfft/2-n] = -m_ws4bm[2*n+1];
			}
			m_Earr4bm[j][0] = m_ws4bm[1];
		}
	}
#ifdef DEBUG_SRC_CHAR
	FILE *fp = file_pointer_debug(DEBUG_BM_SRC_AFT);
	fprintf(fp, "V Ex Ey\n");
	double UV[2];
	UV[0] = U;
	for(int n = 0; n < nfft; n++){
		UV[1] = m_Varr4bm[n];
		fprintf(fp, "%g %g %g\n", m_Varr4bm[n], m_Earr4bm[0][n], m_Earr4bm[1][n]);
	}
	fclose(fp);
#endif
	m_bmsrcfspl[0].SetSpline(nfft, &m_Varr4bm, &m_Earr4bm[0], true);
	m_bmsrcfspl[1].SetSpline(nfft, &m_Varr4bm, &m_Earr4bm[1], true);
}

bool WignerFunction::f_IsEvaluateGtEiwt(bool isx, double range[], double w)
{
	if(isx){
		if(m_type == WignerFuncType2DY || m_type == WignerFuncType3DY){
			return false;
		}
	}
	else{
		if(m_type == WignerFuncType2DX || m_type == WignerFuncType3DX){
			return false;
		}
	}
	if(m_Nwiggler == 0){
		return fabs(w*(range[1]-range[0])) >= MAX_ARG_SN_APPROX;
	}
	return true;
}


double WignerFunction::f_GetOmegaWiggler(int index, double delta)
{
	if(index == 0){
		return 0.0;
	}

	double dindex = (double)(index-1)+delta;
	double dix = (-(double)(m_Nwiggler-1)*0.5+dindex)*(m_isnegpole?-1.0:1.0)+0.25;

	if(m_oddpolewig){
		dix += (m_isnegpole?-1.0:1.0)*0.25;
	}

	return -dix*PI2*2.0*m_eKwiggler;
}

void WignerFunction::f_ReIntegrateEwit(int nc, int np, double w, int N, 
	vector<double> *arg, vector<vector<double>> *values, vector<double> *W)
{
	if(N < 2){
		return;
	}

	double dtau = ((*arg)[1]-(*arg)[0])/(double)(N-1); // 0 = initial, 1 =  final
	double wdtau = w*dtau;
	double wdtauh = wdtau*0.5;
	complex<double> sum(0.0, 0.0), cval, ctex, stex;

	for(int n = 0; n < N; n++){
		cval = complex<double>((*values)[n][2*nc-1], (*values)[n][2*nc]);
		ctex = exp(complex<double>(0.0, w*(*arg)[n]));
		if(n > 1){
			sum += cval*ctex*sincsq(wdtauh);
		}
		else{
			if(fabs(wdtau) < MAX_ARG_SN_APPROX){
				stex =  complex<double>(0.5, 0.0);
			}
			else if(n == 0){
				stex = complex<double>(1.0, wdtau-sin(wdtau));
			}
			else{
				stex = complex<double>(1.0, -wdtau+sin(wdtau));
			}
			sum += cval*ctex*stex;
		}
	}
	sum *= dtau;
	(*W)[2*nc-1+np*2*m_ncomps] = sum.real();
	(*W)[2*nc+np*2*m_ncomps] = sum.imag();
}

void WignerFunction::f_GetWignerAlongUV(
	double uvfix, vector<double> *UVarr, vector<vector<double>> *W,
	int rank, int mpiprocesses)
{
	if(W->size() < UVarr->size()){
		W->resize(UVarr->size());
	}
	for(int n = 0; n < UVarr->size(); n++){
		if((*W)[n].size() < m_nUVpoints){
			(*W)[n].resize(m_nUVpoints);
		}
	}

	m_uvfix[m_uvscidx] = uvfix;

	double uvrange[NumberFStepXrange];
	f_GetFTRange(m_uvscidx, uvrange);

	if(m_sigmaUV[m_uvscidx] > TINY){
		uvrange[FstepXini] = max(uvrange[0], -m_gaussian_limit/m_sigmaUV[m_uvscidx]);
		uvrange[FstepXfin] = min(uvrange[1], m_gaussian_limit/m_sigmaUV[m_uvscidx]);
	}
	if(uvrange[1]-uvrange[0] <= TINY){
		for(int n = 0; n < UVarr->size(); n++){
			fill((*W)[n].begin(), (*W)[n].end(), 0.0);
		}
		return;
	}

	uvrange[FstepDx] = 0;
	uvrange[FstepXref] = uvrange[FstepXini];
	uvrange[FstepXlim] = m_dinterv[m_uvscidx]*1.0e-6;

	vector<double> uv;
	vector<vector<double>> Warr;
	double eps[2] = {0.1/(double)m_acclevel, 0.1/(double)m_acclevel};
	int ninit, steps;

	ninit = (int)ceil(m_gaussian_limit*3)*2+1;
	steps =  RunDigitizer(FUNC_DIGIT_BASE|FUNC_DIGIT_ENABLE_LOG, &uv, &Warr, 
					uvrange, ninit, eps, m_calcstatus, m_process_layer+1, 
					WignerFuncDigitizer, false, false, rank, mpiprocesses); 

	vector<Spline> wspline(2*m_ncomps*m_nUVpoints+1);
	for(int np = 0; np < m_nUVpoints; np++){
		for(int nc = 1; nc <= 2*m_ncomps; nc++){
			wspline[nc+np*2*m_ncomps].SetSpline(steps, &uv, &Warr[nc+np*2*m_ncomps]);
			wspline[nc+np*2*m_ncomps].AllocateGderiv();
		}
	}

#ifdef DEBUG_SRC_CHAR
	FILE *fp = file_pointer_debug(DEBUG_WIGNER_GRGI);
#endif

	vector<complex<double>> G(2*m_ncomps+1);
	double Gr, Gi, wn, w;
	for(int n = 0; n < UVarr->size(); n++){
		w = (*UVarr)[n]*(m_isnegpole?-1.0:1.0)-m_srcpoint[m_uvscidx];
		for(int np = 0; np < m_nUVpoints; np++){
			for(int nc = 1; nc <= m_ncomps; nc++){
				if(m_Nwiggler > 0){
					wn = w-f_GetOmegaWiggler(nc)*m_uvfix[m_uvscidx];
				}
				else{
					wn = w;
				}
				for(int j = 1; j <= 2; j++){
					wspline[2*(nc-1)+j+np*2*m_ncomps].IntegrateGtEiwt(-wn, &Gr, &Gi);
					G[2*(nc-1)+j] = complex<double>(Gr, Gi);
				}
			}
			int ncps = m_ncomps;
			if(m_oddpolewig && !m_isnegpole){ // odd pole number, skip final period for negative pole
				ncps--;
			}
			if(ncps == 0){
				G[0] = G[1] = 0.0;
			}
			for(int nc = 2; nc <= ncps; nc++){
				G[0] += G[2*nc-1];
				G[1] += G[2*nc];
			}
			G[0] = G[0]+complex<double>(0.0, 1.0)*G[1];
			(*W)[n][np] = G[0].real();
#ifdef DEBUG_SRC_CHAR
			fprintf(fp, "%g\t%g\t%g\t%g\n", 
				(*UVarr)[n], m_UVpoints[np], G[0].real(), G[0].imag());
#endif
		}
	}
#ifdef DEBUG_SRC_CHAR
	fclose(fp);
#endif
}

/*
	m_uvfix	: u  , v
	m_uvvar	: u' , v'
	m_uvcv	: u" , v"
*/

void WignerFunction::f_Integrand_u(double u, vector<double> *W)
{
//------>>>>>>
m_rep++;

	double uvp[2], uvm[2], tex, sn;
	complex<double> ctex[2], Wcpx, csn, ew;
	complex<double> emx, emy, epx, epy;
	bool isovld = false;

	m_uvvar[0] = u;

	for(int j = 1; j <= 2 ; j++){
		uvp[j] = m_uvfix[j]-m_uvvar[j]+m_uvcv[j]*0.5;
		uvm[j] = m_uvfix[j]-m_uvvar[j]-m_uvcv[j]*0.5;
		if(m_sigmauv[j] < TINY){
			ctex[j] = complex<double>(1.0, 0.0);
		}
		else{
			tex = m_uvvar[j]/m_sigmauv[j];
			tex *= tex*0.5;
			if(tex > MAXIMUM_EXPONENT){
				ctex[j] = 0.0;
			}
			else{
				ctex[j] = exp(-tex)/(SQRTPI2*m_sigmauv[j]);
			}
		}
	}
	if(m_type == WignerFuncType2DX){
		uvp[1] = uvm[1] = m_uvvar[1];
		ctex[1] = complex<double>(1.0, 0.0);
	}
	else if(m_type == WignerFuncType2DY){
		uvp[0] = uvm[0] = m_uvvar[0];
		ctex[0] = complex<double>(1.0, 0.0);
	}
	else if(m_type == WignerFuncType3DX){
		uvp[1] = uvm[1] = m_uvfix[1]-m_uvvar[1];
	}
	else if(m_type == WignerFuncType3DY){
		uvp[0] = uvm[0] = m_uvfix[0]-m_uvvar[0];
	}

	Wcpx = ctex[0]*ctex[1];
	if(abs(Wcpx) > TINY){
		GetExyAmplitude(uvp, &epx, &epy);
		GetExyAmplitude(uvm, &emx, &emy);
		ew = conj(epx)*emx+conj(epy)*emy;
		if(m_isund){
			double uu[2] = {uvm[0], uvp[0]};
			double vv[2] = {uvm[1], uvp[1]};
#ifdef DEFINE_UR_GAUSSIAN
			sn = exp(-hypotsq(uvm[0], uvm[1]))*exp(-hypotsq(uvp[0], uvp[1]));
#else
			sn = GetSn(uu, vv);
#endif
		}
		else{
			sn = 1.0;
		}
		Wcpx *= ew*sn;
	}

	for(int nc = 1; nc <= m_ncomps; nc++){
		(*W)[2*nc-1] = Wcpx.real();
		(*W)[2*nc] = Wcpx.imag();
	}
}

void WignerFunction::f_Integrand_v(double v, vector<double> *W)
{
	double urange[2];
	int layers[2] = {WignerIntegOrderU, -1};
	m_uvvar[1] = v;

	if(m_type == WignerFuncType2DY){
		urange[0] = -m_halfrange[0];
		urange[1] = m_halfrange[0];
	}
	else if(m_sigmauv[0] < TINY){
		QSimpsonIntegrand(WignerIntegOrderU, 0.0, W);
		return;
	}
	else{
		f_GetIntegRangeCV(1, urange);
		urange[0] = max(urange[0], -m_gaussian_limit*m_sigmauv[0]);
		urange[1] = min(urange[1], m_gaussian_limit*m_sigmauv[0]);
		if(urange[1]-urange[0] < TINY){
			f_PutZeroValues(W);
			return;
		}
	}

	int qlevel[2];
	f_GetIntegralLevel(urange, 1, qlevel);

	IntegrateSimpson(layers, urange[0], urange[1], 0.1/(double)m_acclevel, 
		qlevel[0], nullptr, W, WignerIntegAlong_u, false, true, qlevel[1]);

	double w = m_alpha[0]*m_uvcv[0], wn;
	if(f_IsEvaluateGtEiwt(true, urange, w)){
		int N = GetEvaluatedValue(WignerIntegOrderU, 
			&m_wsarg[WignerIntegOrderU], &m_wsval[WignerIntegOrderU], WignerIntegAlong_u);
		for(int nc = 1; nc <= m_ncomps; nc++){
			if(m_Nwiggler > 0){
				wn = w+f_GetOmegaWiggler(nc)*m_uvcv[0];
			}
			else{
				wn = w;
			}
			f_ReIntegrateEwit(nc, 0, -wn, N, &m_wsarg[WignerIntegOrderU], &m_wsval[WignerIntegOrderU], W);
		}
	}

	for(int nc = 1; nc <= 2*m_ncomps; nc++){
		if(fabs((*W)[nc]) > m_currmaxref[WignerIntegOrderV]){
			m_currmaxref[WignerIntegOrderV] = fabs((*W)[nc]);
		}
	}
}

void WignerFunction::f_Convolute_uv(int uvidx, double uv, vector<double> *W)
{
//----->>>>>
	m_rep=0;

	double vrange[2], tex, itex;
	complex<double>	ctex;
	int layers[2] = {WignerIntegOrderV, -1};
	m_uvcv[uvidx] = uv;

	if(m_type == WignerFuncType4DX || m_type == WignerFuncType4DY || m_type == WignerFuncTypeXY){
		tex = uv*m_sigmaUV[uvidx];
		tex *= tex*0.5;
		if(tex > MAXIMUM_EXPONENT){
			f_PutZeroValues(W);
			return;
		}
		itex = 0.0;
		ctex = exp(complex<double>(-tex, -itex));
	}
	else{
		ctex = complex<double>(1.0, 0.0);
	}

	if(ctex.real() == 0){
		f_PutZeroValues(W);
		return;
	}

	if(m_type != WignerFuncType2DX && m_sigmauv[1] < TINY){
		QSimpsonIntegrand(WignerIntegOrderV, 0.0, W);
	}
	else{
		if(m_type == WignerFuncType2DX){
			vrange[0] = -m_halfrange[1];
			vrange[1] = m_halfrange[1];
		}
		else{
			f_GetIntegRangeCV(2, vrange);
			vrange[0] = max(vrange[0], -m_gaussian_limit*m_sigmauv[1]);
			vrange[1] = min(vrange[1], m_gaussian_limit*m_sigmauv[1]);
			if(vrange[1]-vrange[0] < TINY){
				f_PutZeroValues(W);
				return;
			}
		}

		//QSimpsonIntegrand(WignerIntegOrderV, -0.00721648, W);

		int qlevel[2];
		f_GetIntegralLevel(vrange, 2, qlevel);

		layers[0] = m_process_layer+2;
		IntegrateSimpson(layers, vrange[0], vrange[1], 0.2/(double)m_acclevel, 
			qlevel[0], nullptr, W, WignerIntegAlong_v, false, true, qlevel[1]);

		double w = m_alpha[1]*m_uvcv[1], wn;
		if(f_IsEvaluateGtEiwt(false, vrange, w)){
			int N = GetEvaluatedValue(WignerIntegOrderV, 
				&m_wsarg[WignerIntegOrderV], &m_wsval[WignerIntegOrderV], WignerIntegAlong_v);
			for(int nc = 1; nc <= m_ncomps; nc++){
				if(m_Nwiggler > 0){
					wn = w+f_GetOmegaWiggler(nc)*m_uvcv[1];
				}
				else{
					wn = w;
				}
				f_ReIntegrateEwit(nc, 0, -wn, N, &m_wsarg[WignerIntegOrderV], &m_wsval[WignerIntegOrderV], W);
			}

		}
	}

	for(int nc = 1; nc <= m_ncomps; nc++){
		complex<double> w((*W)[2*nc-1], (*W)[2*nc]);
		w *= ctex;
		(*W)[2*nc-1] = w.real();
		(*W)[2*nc] = w.imag();
	}
}

void WignerFunction::f_GetIntegRangeCV(int uvidx, double uvrange[])
{
	double range = m_halfrange[uvidx];

	if(m_uvcv[uvidx] < 0){
		uvrange[0] = m_uvfix[uvidx]-m_uvcv[uvidx]*0.5-range;
		uvrange[1] = m_uvfix[uvidx]+m_uvcv[uvidx]*0.5+range;
	}
	else{
		uvrange[0] = m_uvfix[uvidx]+m_uvcv[uvidx]*0.5-range;
		uvrange[1] = m_uvfix[uvidx]-m_uvcv[uvidx]*0.5+range;
	}
}

void WignerFunction::f_GetFTRange(int uvidx, double uvrange[])
{
	double valrange = m_halfrange[uvidx]*2.0;
	uvrange[0] = 2.0*fabs(m_uvfix[uvidx])-valrange-m_gaussian_limit*m_sigmauv[uvidx];
	uvrange[1] = -2.0*fabs(m_uvfix[uvidx])+valrange+m_gaussian_limit*m_sigmauv[uvidx];
}

void WignerFunction::f_PutZeroValues(vector<double> *W, int np)
{
	for(int nc = 1; nc <= m_ncomps*np; nc++){
		(*W)[2*nc-1] = (*W)[2*nc] = 0.0;
	}
}

int WignerFunction::f_GetSkipNumber(double *data, int nfft, bool isamp)
{
	int nskip = 0;
	double eps = 0, smax = 0, dsmax, ssa, ssb, tgtacc;

	for(int n = -nfft/2; n <= nfft/2; n++){
		int ix = fft_index(n, nfft, -1);
		smax = max(smax, hypotsq(data[2*ix], data[2*ix+1]));
	}

	tgtacc = isamp ? 0.02 : 0.04;

	while(eps < tgtacc/(double)max(1, m_acclevel/4)){
		if(nskip == 0){
			nskip = 1;
		}
		else{
			nskip <<= 1;
		}
		dsmax = 0.0;
		for(int n = -nfft/2; n <= nfft/2; n+= nskip){
			int ix = fft_index(n, nfft, -1);
			if(n == -nfft/2){
				ssa = hypotsq(data[2*ix], data[2*ix+1]);
			}
			else{
				ssb = hypotsq(data[2*ix], data[2*ix+1]);
				dsmax = max(dsmax, fabs(ssa-ssb));
				ssa = ssb;
			}
		}
		eps = dsmax/smax;
	}
	return nskip;
}

void WignerFunction::f_GetIntegralLevel(double uvrange[], int uvidx, int level[])
{
	double meshnum = fabs(uvrange[1]-uvrange[0])/m_dinterv[uvidx]/2.0;
	int basel = (int)ceil(log10(meshnum+TINY)/LOG2);
	level[0] = m_acclevel+max(4, basel);	
	level[1] = min(15, level[0]+m_acclevel+3);
}

void WignerFunction::f_AllocateEwxyAxis(
	int ndatapoints, int nc, vector<double> *values,	bool isodd, int halfmesh, double dtheta, 
	int jxy, vector<complex<double>> *Ewx, vector<complex<double>> *Ewy, FluxDensity *fluxdens)
{
	double theta[2] = {0, 0};
	int nxr, nxi, nyr, nyi;

	nxr = nc;
	nxi = nc+ndatapoints;
	nyr = nc+2*ndatapoints;
	nyi = nc+3*ndatapoints;

	for(int n = isodd?1:0; n <= 2*halfmesh; n += 2){
		theta[jxy] = (double)(n-halfmesh)*dtheta;
		fluxdens->GetFluxItemsAt(theta, values, true);
		(*Ewx)[n] = complex<double>((*values)[nxr], (*values)[nxi]);
		(*Ewy)[n] = complex<double>((*values)[nyr], (*values)[nyi]);
	}
}

void WignerFunction::f_AssignSpRange()
{
	double eaxis, fr;
	int c[2];

	for(int j = 1; j <= 2; j++){
		c[j] = (m_spmesh[j][0]-1)/2;
		m_speini[j] = -1;
		m_spefin[j] = m_spmesh[j][0]; 
	}

	eaxis = m_e[0][c[0]][c[1]];

	for(int j = 1; j <= 2; j++){
		do{
			m_speini[j]++;
			if(j == 1){
				fr = m_e[0][m_speini[0]][c[1]];
			}
			else{
				fr = m_e[0][c[0]][m_speini[1]];
			}
		}while(fr < eaxis*0.01);
		do{
			m_spefin[j]--;
			if(j == 1){
				fr = m_e[0][m_spefin[0]][c[1]];
			}
			else{
				fr = m_e[0][c[0]][m_spefin[1]];
			}
		}while(fr < eaxis*0.01);

		if((m_spefin[j]-m_speini[j]+1)%2 == 0){
			m_spefin[j]--;
		}
	}

#ifdef DEBUG_SRC_CHAR_A
	double UV[2];
	FILE *fp = file_pointer_debug(DEBUG_REDUCED_SRCPROFILE);
	for(int ix = m_speini[0]; ix <= m_spefin[0]; ix++){
		UV[0] = (double)(ix-m_halfmeshsp[0][0])*m_deltasp[0][0];
		for(int iy = m_speini[1]; iy <= m_spefin[1]; iy++){
			UV[1] = (double)(iy-m_halfmeshsp[1][0])*m_deltasp[1][0];
			fprintf(fp, "%g\t%g\t%g\n", UV[0], UV[1], m_e[0][ix][iy]);
		}
	}
	fclose(fp);
#endif
}
