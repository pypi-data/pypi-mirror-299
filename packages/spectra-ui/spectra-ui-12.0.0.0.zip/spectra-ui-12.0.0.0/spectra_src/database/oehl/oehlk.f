c    main program
      program oehlk
      implicit real*8 (a-h,o-z)
c
c ---- file(1): input the source flux; file(2): output the flux after
c      the filter ; file(3): filter control file; file(4): material data file
c      file(7): output summary file
c      
      character*16 funit1,funit2,funit3,funit7
      common/data/e(100000),flux(100000,10),nmax
      common/idata/zn,an,alp1,alp2,d,theta,den,aw,cont
c                                                                       
c  -- input data: zn: atomic number; an, alp1,alp2, density             
c  -- parameters; d: material thickness (cm); theta: incident           
c  -- angle with the surface (degree); den: material density            
c  -- (g/cmm**3); aw: atomic weigth.                                    
c     call ireads, iread3, pdata, filter                                
c                                                                       
c ----- input spectra of radiation source
c
      write(6,*) 'please input the file name of unit 1: (input)'
      read(5,*) funit1
      open(1,file=funit1,status='old')
      if(ireads(1).ne.1) stop ' stop in ireads function '
      close(1)
      write(6,*) 'please input the file name of unit 2: (output)'
      read(5,*) funit2
      open(2,file=funit2,status='unknown')
      write(6,*) 'please input the file name of unit 7: (summary)'
      read(5,*) funit7
      open(7,file=funit7,status='unknown')
      write(6,*) 'please input the file name of unit 3: (filter)'
      read(5,*) funit3
      write(2,*)'No Angle  Input   Output  Absorbed Compton back/trans
     1 Rayleigh back/tr  Heat'
      open(3,file=funit3,status='old')
      read(3,'(2x,i5)') mfile
      do 1 i=1,mfile
         call iread3
         call pdata
         call filter(i)
 1    continue
      close(3)
      write(2,*)' ENERGY(eV)  SOURCE FLUX   1st FLUX   2nd FLUX'
      do 3 i=1,nmax
         write(2,'(11(1pe12.4e3))') e(i),(flux(i,j),j=1,mfile+1)
 3    continue
      close(2)
      close(7)
      stop
      end
c                                                                       
      subroutine filter(ith)
c                                                                       
      implicit real*8 (a-h,o-z)
      external cbsf,ctsf,rbsf,rtsf
      common/data/e(100000),flux(100000,10),nmax
      common/idata/zn,an,alp1,alp2,d,theta,den,aw,cont
      common/tdata/u(100000),apk(100000),temp(100000),uk,wk
      common/temp/w,uw,dsthe,dcthe
      data emax,emin,pi,r02,n16/174.0d0,5.747d-3,3.1415926,
     1 7.9438142d-02,16/
      save
      zero=0.d0
      one=1.d0
c     
c --- transmitted spectra                                               
c                                                                       
      if(theta.eq.0) goto 20
      ang  =theta / 0.0174532
      write(7,106) ith,zn,ang,d
      call power(e,flux(1,ith),nmax,powin)
      dd = d/dsin(theta)
      ithp1 = ith + 1
      do 1 i = 1, nmax
         flux(i,ithp1) = flux(i,ith) * dexp(-u(i)*dd)
  1   continue
      call power(e,flux(1,ithp1),nmax,trpow)
      powab=powin-trpow
      write(7,101) powin,trpow,powab
c                                                                       
c --- radiative decay back to the surface                               
c                                                                       
      ukd=uk * d
      dsthe=dsin(theta)
      dcthe=dcos(theta)
      do 2 i=1,nmax
         x=uk/u(i)*dsthe
         a1=1.0-x*dlog(1.d0+1.d0/x)
         x=dsthe/u(i)/d
         a2=0.0
         if(ukd.le.emax.or.x.ge.emin) then a2=dexp(-1.0/x)*fgauin(ukd,x)*udk
         temp(i)=flux(i,ith)*apk(i)/e(i)*(a1-a2)
  2   continue
      call power(e,temp,nmax,dpb)
      dpb = dpb * 0.5 * wk
c                                                                       
c ----radiative decay tran. the material                                
c                                                                       
      do 3 i=1,nmax
         x=uk/u(i)*dsthe
         a1=(1.0+x*dlog(dabs(1.d0-1.d0/x)))* dexp(-u(i)*d/dsthe)
         x=-dsthe/u(i)/d
         a2=0.0
         if(ukd.le.emax) then a2=udk * fgauin(udk,x)
         temp(i)=flux(i,ith)*apk(i)/e(i)*(a2-a1)
  3   continue
      call power(e,temp,nmax,dpt)
      dpt = dpt * 0.5 * wk
      write(7,102) dpb, dpt
c                                                                       
c   --- back scattered of compton scattering                            
c                                                                       
      do 4 i=1,nmax
         w=e(i)
         uw=u(i)
         call dgaus2(cbsf,zero,one,zero,pi,n16,n16,v)
         temp(i)=flux(i,ith)/w/u(i)*v
  4   continue
      call power(e,temp,nmax,cpb)
      cpb=cpb * zn * cont * r02
c                                                                       
c ---- trans. power of compton scattering                               
c                                                                       
      do 5 i=1,nmax
         w=e(i)
         uw=u(i)
         call dgaus2(ctsf,zero,one,zero,pi,n16,n16,v)
         temp(i)=flux(i,ith)/w/u(i)*v
  5   continue
      call power(e,temp,nmax,cpt)
      cpt=cpt * zn * cont * r02
      write(7,103) cpb,cpt
c                                                                       
c ---- back scattering of rayleigh process                              
c                                                                       
      do 6 i=1,nmax
         w=e(i)
         uw=u(i)
         call dgaus2(rbsf,zero,one,zero,pi,n16,n16,v)
         temp(i)=flux(i,ith)/u(i)*v
  6   continue                                                          
      call power(e,temp,nmax,rpb)
      rpb = rpb * zn * zn * cont * r02
c                                                                       
c ---- tran. scattering of rayleigh process                             
c                                                                       
      do 7 i=1,nmax
         w=e(i)
         uw=u(i)
         call dgaus2(rtsf,zero,one,zero,pi,n16,n16,v)
         temp(i)=flux(i,ith)/u(i)*v
  7   continue
      call power(e,temp,nmax,rpt)
      rpt = rpt * zn * zn * cont * r02
      hpow=powab-cpb-cpt-rpb-rpt
      write(6,107) ith,ang,powab,cpb,cpt,rpb,rpt,hpow
      write(7,104) rpb,rpt
      write(2,107) ith,ang,powin,trpow,powab,cpb,cpt,rpb,rpt,hpow
      return
  20  write(6,100)
 100  format(1x,'the incident angle is zero.
     1 pls check it')
 101  format(1x,'the input power is ',f8.4,' kw the output power is ',
     1 f8.4,' kw'/1x,'the absor.power is ',f8.4,' kw'/ )
 102  format(1x,'the back  power is ',f8.4,' kw the trans. power is ',
     1 f8.4,' kw'/1x,' by radiative decay process * wk'/ )
 103  format(1x,'the back  power is ',f8.4,' kw the trans. power is ',
     1 f8.4,' kw'/1x,' by compton process '/ )
 104  format(1x,'the back  power is ',f8.4,' kw the trans. power is ',
     1 f8.4,' kw'/1x,' by rayleigh  process '/ )
 106  format(1x,' the materail parameters of the ',i2,'th filter' / / 
     1 1x,' atomic number = ',f7.2, '      angle =',f7.2,'degree'/ /
     2 1x,'thickness     = ',f7.2, 'cm; '/)
       stop ' stop in the filter subroutine'
 107  format(1x,i1,f5.1,2(1x,f8.4),6(1x,f8.5))
c                                                                       
      end
c                                                                       
      function cbsf(x,y)                                                
      implicit real*8 (a-h,o-z)                                         
      common/idata/zn,an,alp1,alp2,d,theta,den,aw,cont                  
      common/temp/w,uw,dsthe,dcthe                                      
      cbsf=0.d0                                                         
      if(x.eq.0.d0) return                                              
      dsi=dsqrt(1.0-x*x)                                                
      cs=-dsi*dcos(y)*dcthe-dsthe*x                                     
      sc=dcthe*x-dsthe*dsi*dcos(y)                                      
      w1=w/(1.0+w/511000.d0*(1.0-cs))                                   
      w1h=w1/1000.0                                                     
      uw1=ucoe(w1h)                                                     
      x1=w1/w                                                           
      cbsf=x1*x1*(x1+1.d0/x1-2.0*sc*sc)/(1.d0+uw1*dsthe/uw/x)           
     1 *(1.d0-dexp(-(uw/dsthe+uw1/x)*d))*w1                             
      return                                                            
      end                                                               
c                                                                       
      function ctsf(x,y)                                                
      implicit real*8 (a-h,o-z)                                         
      common/idata/zn,an,alp1,alp2,d,theta,den,aw,cont                  
      common/temp/w,uw,dsthe,dcthe                                      
      ctsf=0.d0                                                         
      if(x.eq.0.d0) return                                              
      dsi=dsqrt(1.0-x*x)                                                
      cs=-dsi*dcos(y)*dcthe+dsthe*x                                     
      sc=-dcthe*x-dsthe*dsi*dcos(y)                                     
      w1=w/(1.0+w/511000.d0*(1.0-cs))                                   
      w1h=w1/1000.0                                                     
      uw1=ucoe(w1h)                                                     
      x1=w1/w                                                           
      ctsf=x1*x1*(x1+1.d0/x1-2.0*sc*sc)/(1.d0-uw1*dsthe/uw/x)           
     1 *(dexp(-uw1/x*d)-dexp(-uw/dsthe*d))*w1                           
      return                                                            
      end                                                               
c                                                                       
      function rbsf(x,y)                                                
      implicit real*8 (a-h,o-z)                                         
      common/idata/zn,an,alp1,alp2,d,theta,den,aw,cont                       
      common/temp/w,uw,dsthe,dcthe                                      
      rbsf=0.d0                                                         
      if(x.eq.0.d0) return                                              
      a2=alp1*alp1                                                      
      a22=alp2*alp2                                                     
      dsi=dsqrt(1.d0-x*x)                                               
      cs=-dsi*dcos(y)*dcthe-dsthe*x                                     
      q2=2.d0*(1.d0-cs)*(w/137.d0/27.2d0)**2                            
      f=an*a2/(a2+q2)+(1.d0-an)*a22/(a22+q2)                            
      rbsf=f*f*(1.d0+cs*cs)/(1.d0+dsthe/x)                              
     1   *(1.d0-dexp(-uw/dsthe*d-uw/x*d))                               
      return                                                            
      end                                                               
c                                                                       
      function rtsf(x,y)                                                
      implicit real*8 (a-h,o-z)                                         
      common/idata/zn,an,alp1,alp2,d,theta,den,aw,cont                       
      common/temp/w,uw,dsthe,dcthe                                      
      rtsf=0.d0                                                         
      if(x.eq.0.d0) return                                              
      a2=alp1*alp1                                                      
      a22=alp2*alp2                                                     
      dsi=dsqrt(1.0-x*x)                                                
      cs=-dsi*dcos(y)*dcthe+dsthe*x                                     
      q2=2.d0*(1.d0-cs)*(w/137.d0/27.2d0)**2                            
      f=an*a2/(a2+q2)+(1.d0-an)*a22/(a22+q2)                            
      rtsf=f*f*(1.d0+cs*cs)/(1.d0-dsthe/x)                              
     1   *(dexp(-uw/x*d)-dexp(-uw/dsthe*d))                             
      return                                                            
      end                                                               
c                                                                       
      function  fgauin(a,x)                                             
      implicit real*8 (a-h,o-z)                                         
c                                                                       
      dimension c(12),w(12)                                             
c                                                                       
      data c/ 0.1157221173580207d+00, 0.6117574845151305d+00,           
     $        0.1512610269776419d+01, 0.2833751337743508d+01,           
     $        0.4599227639418349d+01, 0.6844525453115177d+01,           
     $        0.9621316842456867d+01, 0.1300605499330635d+02,           
     $        0.1711685518746226d+02, 0.2215109037939700d+02,           
     $        0.2848796725098400d+02, 0.3709912104446692d+02/           
      data w/ 0.2647313710554374d+00, 0.3777592758731376d+00,           
     $        0.2440820113198780d+00, 0.9044922221168090d-01,           
     $        0.2010238115463409d-01, 0.2663973541865317d-02,           
     $        0.2032315926629994d-03, 0.8365055856819797d-05,           
     $        0.1668493876540909d-06, 0.1342391030515007d-08,           
     $        0.3061601635035027d-11, 0.8148077467426254d-15/           
c                                                                       
      v = 0                                                             
      do 10 i = 1, 12                                                   
      x1=a+c(i)                                                         
        v = v + w(i)/(1.0+x*x1)/x1/x1                                   
   10 continue                                                          
c                                                                       
      fgauin = exp(-a) * v                                              
      return                                                            
      end                                                               
c
      subroutine dgaus2 (func, a, b, c, d, m, n, v)                     
*****************************************************                   
*           legendre-gauss product formula          *                   
*       over 2-dimensional rectangular domain       *                   
*      copyright : m.mori  june 30 1989  v.1        *                   
*   ---- input parameters ----                      *                   
*     func = name of the function subprogram for    *                   
*            the integrand                          *                   
*     a = lower bound of the first variable         *                   
*     b = upper bound of the first variable         *                   
*     c = lower bound of the second variable        *                   
*     d = upper bound of the second variable        *                   
*     m = number of points for the first variable   *                   
*         not larger than 16                        *                   
*     n = number of points for the second variable  *                   
*         not larger than 16                        *                   
*   ---- output parameter ----                      *                   
*     v ... result of integration                   *                   
*****************************************************                   
      implicit real*8 (a-h,o-z)                                         
*                                                                       
      external func
      dimension p(0:8,16),w(0:8,16)                                     
*                                                                       
      data (p(i, 1),i=0, 0) /                                           
     $   0.0000000000000000d+00 /                                       
      data (w(i, 1),i=0, 0) /                                           
     $   0.2000000000000000d+01 /                                       
      data (p(i, 2),i=1, 1) /                                           
     $   0.5773502691896257d+00 /                                       
      data (w(i, 2),i=1, 1) /                                           
     $   0.9999999999999998d+00 /                                       
      data (p(i, 3),i=0, 1) /                                           
     $   0.0000000000000000d+00,                                        
     $   0.7745966692414832d+00 /                                       
      data (w(i, 3),i=0, 1) /                                           
     $   0.8888888888888888d+00,                                        
     $   0.5555555555555558d+00 /                                       
      data (p(i, 4),i=1, 2) /                                           
     $   0.3399810435848563d+00,                                        
     $   0.8611363115940525d+00 /                                       
      data (w(i, 4),i=1, 2) /                                           
     $   0.6521451548625459d+00,                                        
     $   0.3478548451374539d+00 /                                       
      data (p(i, 5),i=0, 2) /                                           
     $   0.0000000000000000d+00,                                        
     $   0.5384693101056831d+00,                                        
     $   0.9061798459386639d+00 /                                       
      data (w(i, 5),i=0, 2) /                                           
     $   0.5688888888888888d+00,                                        
     $   0.4786286704993666d+00,                                        
     $   0.2369268850561892d+00 /                                       
      data (p(i, 6),i=1, 3) /                                           
     $   0.2386191860831969d+00,                                        
     $   0.6612093864662644d+00,                                        
     $   0.9324695142031520d+00 /                                       
      data (w(i, 6),i=1, 3) /                                           
     $   0.4679139345726909d+00,                                        
     $   0.3607615730481386d+00,                                        
     $   0.1713244923791703d+00 /                                       
      data (p(i, 7),i=0, 3) /                                           
     $   0.0000000000000000d+00,                                        
     $   0.4058451513773972d+00,                                        
     $   0.7415311855993944d+00,                                        
     $   0.9491079123427584d+00 /                                       
      data (w(i, 7),i=0, 3) /                                           
     $   0.4179591836734694d+00,                                        
     $   0.3818300505051189d+00,                                        
     $   0.2797053914892767d+00,                                        
     $   0.1294849661688699d+00 /                                       
      data (p(i, 8),i=1, 4) /                                           
     $   0.1834346424956498d+00,                                        
     $   0.5255324099163289d+00,                                        
     $   0.7966664774136267d+00,                                        
     $   0.9602898564975361d+00 /                                       
      data (w(i, 8),i=1, 4) /                                           
     $   0.3626837833783622d+00,                                        
     $   0.3137066458778873d+00,                                        
     $   0.2223810344533746d+00,                                        
     $   0.1012285362903763d+00 /                                       
      data (p(i, 9),i=0, 4) /                                           
     $   0.0000000000000000d+00,                                        
     $   0.3242534234038089d+00,                                        
     $   0.6133714327005903d+00,                                        
     $   0.8360311073266357d+00,                                        
     $   0.9681602395076260d+00 /                                       
      data (w(i, 9),i=0, 4) /                                           
     $   0.3302393550012598d+00,                                        
     $   0.3123470770400028d+00,                                        
     $   0.2606106964029356d+00,                                        
     $   0.1806481606948573d+00,                                        
     $   0.8127438836157435d-01 /                                       
      data (p(i,10),i=1, 5) /                                           
     $   0.1488743389816312d+00,                                        
     $   0.4333953941292473d+00,                                        
     $   0.6794095682990244d+00,                                        
     $   0.8650633666889845d+00,                                        
     $   0.9739065285171717d+00 /                                       
      data (w(i,10),i=1, 5) /                                           
     $   0.2955242247147527d+00,                                        
     $   0.2692667193099963d+00,                                        
     $   0.2190863625159819d+00,                                        
     $   0.1494513491505806d+00,                                        
     $   0.6667134430868799d-01 /                                       
      data (p(i,11),i=0, 5) /                                           
     $   0.0000000000000000d+00,                                        
     $   0.2695431559523450d+00,                                        
     $   0.5190961292068118d+00,                                        
     $   0.7301520055740493d+00,                                        
     $   0.8870625997680953d+00,                                        
     $   0.9782286581460569d+00 /                                       
      data (w(i,11),i=0, 5) /                                           
     $   0.2729250867779006d+00,                                        
     $   0.2628045445102467d+00,                                        
     $   0.2331937645919905d+00,                                        
     $   0.1862902109277342d+00,                                        
     $   0.1255803694649046d+00,                                        
     $   0.5566856711617373d-01 /                                       
      data (p(i,12),i=1, 6) /                                           
     $   0.1252334085114689d+00,                                        
     $   0.3678314989981802d+00,                                        
     $   0.5873179542866174d+00,                                        
     $   0.7699026741943046d+00,                                        
     $   0.9041172563704747d+00,                                        
     $   0.9815606342467192d+00 /                                       
      data (w(i,12),i=1, 6) /                                           
     $   0.2491470458134029d+00,                                        
     $   0.2334925365383548d+00,                                        
     $   0.2031674267230659d+00,                                        
     $   0.1600783285433463d+00,                                        
     $   0.1069393259953185d+00,                                        
     $   0.4717533638651187d-01 /                                       
      data (p(i,13),i=0, 6) /                                           
     $   0.0000000000000000d+00,                                        
     $   0.2304583159551348d+00,                                        
     $   0.4484927510364469d+00,                                        
     $   0.6423493394403402d+00,                                        
     $   0.8015780907333098d+00,                                        
     $   0.9175983992229779d+00,                                        
     $   0.9841830547185881d+00 /                                       
      data (w(i,13),i=0, 6) /                                           
     $   0.2325515532308739d+00,                                        
     $   0.2262831802628972d+00,                                        
     $   0.2078160475368886d+00,                                        
     $   0.1781459807619456d+00,                                        
     $   0.1388735102197873d+00,                                        
     $   0.9212149983772848d-01,                                        
     $   0.4048400476531587d-01 /                                       
      data (p(i,14),i=1, 7) /                                           
     $   0.1080549487073436d+00,                                        
     $   0.3191123689278898d+00,                                        
     $   0.5152486363581540d+00,                                        
     $   0.6872929048116854d+00,                                        
     $   0.8272013150697650d+00,                                        
     $   0.9284348836635735d+00,                                        
     $   0.9862838086968123d+00 /                                       
      data (w(i,14),i=1, 7) /                                           
     $   0.2152638534631578d+00,                                        
     $   0.2051984637212956d+00,                                        
     $   0.1855383974779379d+00,                                        
     $   0.1572031671581936d+00,                                        
     $   0.1215185706879031d+00,                                        
     $   0.8015808715976016d-01,                                        
     $   0.3511946033175195d-01 /                                       
      data (p(i,15),i=0, 7) /                                           
     $   0.0000000000000000d+00,                                        
     $   0.2011940939974345d+00,                                        
     $   0.3941513470775634d+00,                                        
     $   0.5709721726085388d+00,                                        
     $   0.7244177313601700d+00,                                        
     $   0.8482065834104272d+00,                                        
     $   0.9372733924007058d+00,                                        
     $   0.9879925180204854d+00 /                                       
      data (w(i,15),i=0, 7) /                                           
     $   0.2025782419255613d+00,                                        
     $   0.1984314853271116d+00,                                        
     $   0.1861610000155623d+00,                                        
     $   0.1662692058169940d+00,                                        
     $   0.1395706779261542d+00,                                        
     $   0.1071592204671719d+00,                                        
     $   0.7036604748810814d-01,                                        
     $   0.3075324199611710d-01 /                                       
      data (p(i,16),i=1, 8) /                                           
     $   0.9501250983763744d-01,                                        
     $   0.2816035507792589d+00,                                        
     $   0.4580167776572274d+00,                                        
     $   0.6178762444026437d+00,                                        
     $   0.7554044083550029d+00,                                        
     $   0.8656312023878317d+00,                                        
     $   0.9445750230732326d+00,                                        
     $   0.9894009349916499d+00 /                                       
      data (w(i,16),i=1, 8) /                                           
     $   0.1894506104550686d+00,                                        
     $   0.1826034150449236d+00,                                        
     $   0.1691565193950025d+00,                                        
     $   0.1495959888165767d+00,                                        
     $   0.1246289712555339d+00,                                        
     $   0.9515851168249285d-01,                                        
     $   0.6225352393864789d-01,                                        
     $   0.2715245941175410d-01 /                                       
      save
*     
      if ((m. lt. 1) .or. (m .gt. 16)) go to 901                        
      if ((n. lt. 1) .or. (n .gt. 16)) go to 901                        
*                                                                       
      cx1 = (b + a) / 2                                                 
      cx2 = (b - a) / 2                                                 
      cy1 = (d + c) / 2                                                 
      cy2 = (d - c) / 2                                                 
*                                                                       
      if (mod(m,2) .eq. 0) then                                         
        ms = 1                                                          
        mh = m / 2                                                      
      else                                                              
        ms = 0                                                          
        mh = (m - 1) / 2                                                
      end if                                                            
*                                                                       
      if (mod(n,2) .eq. 0) then                                         
        ns = 1                                                          
        nh = n / 2                                                      
      else                                                              
        ns = 0                                                          
        nh = (n - 1) / 2                                                
      end if                                                            
*                                                                       
      if ((ms .ne. 0) .and. (ns .ne. 0)) then                           
        v = 0                                                           
      else if (ms .eq. 0) then                                          
        if (ns .ne. 0) then                                             
          v = 0                                                         
        else                                                            
          v = w(0,m) * w(0,n) * func(cx1,cy1)                           
          do 30 i = 1, mh                                               
            v = v + w(i,m) * w(0,n)                                     
     $            * (func(cx1 + cx2 * p(i,m),cy1)                       
     $             + func(cx1 - cx2 * p(i,m),cy1))                      
   30     continue                                                      
        end if                                                          
        do 40 j = 1, nh                                                 
          v = v + w(0,m) * w(j,n)                                       
     $          * (func(cx1, cy1 + cy2 * p(j,n))                        
     $           + func(cx1, cy1 - cy2 * p(j,n)))                       
   40   continue                                                        
      else if (ns .eq. 0) then                                          
        v = 0                                                           
        do 50 i = 1, mh                                                 
          v = v + w(i,m) * w(0,n)                                       
     $          * (func(cx1 + cx2 * p(i,m), cy1)                        
     $           + func(cx1 - cx2 * p(i,m), cy1))                       
   50   continue                                                        
      end if                                                            
*                                                                       
      do 10 i = 1, mh                                                   
        do 20 j = 1, nh                                                 
          v = v + w(i,m) * w(j,n)                                       
     $     * (func(cx1 + cx2 * p(i,m), cy1 + cy2 * p(j,n))              
     $      + func(cx1 + cx2 * p(i,m), cy1 - cy2 * p(j,n))              
     $      + func(cx1 - cx2 * p(i,m), cy1 + cy2 * p(j,n))              
     $      + func(cx1 - cx2 * p(i,m), cy1 - cy2 * p(j,n)))             
   20   continue                                                        
   10 continue                                                          
*                                                                       
      v = cx2 * cy2 * v                                                 
*                                                                       
      return                                                            
*                                                                       
  901 continue                                                          
      write (6,2001) m, n                                               
 2001 format (' (subr.dgaus2) invalid argument',                        
     $        ' m =',i4,' or n =',i4)                                   
      return                                                            
*                                                                       
      end                                                               
c
      subroutine power(x,y,n,result)                               
      implicit real*8 (a-h,o-z)                                         
      dimension x(n),y(n)                                               
      dx=0.0                                                            
      sum=0.0                                                           
      do 4 i=1,n-1                                                       
         dx=x(i)-x(i+1)                                                        
         sum=sum+dx*(y(i+1)+y(i))/2
 4    continue                                                          
      result=sum*1.602d-19                                 
      return                                                            
      end                                                               
c                                                                       
      subroutine iread3                 
c                                                                       
c ---  called by main, call input (photon cross section)                
c                                                                       
      implicit real*8 (a-h,o-z)                                         
      character*30 fname                                                
      common/idata/zn,an,alp1,alp2,d,theta,den,aw,cont                  
      name list/data/fname,d,theta,den,zn,aw,an,alp1,alp2               
      read(3,data)
      open(4,file=fname,status='old')                                   
      call input(4)                                                     
      close(4)                                                          
      return                                                            
      end                                                               
c                                                                       
      
      function   ireads(ir1)                                            
c                                                                       
c --- this program is used to read and check the spectra data           
c     called by main.                                                   
c                                                                       
      implicit real*8 (a-h,o-z)                                         
      character*10 begin
      common/data/e(100000),flux(100000,10),nmax                  
      i=0                                                               
      ireads=0                                                          
   10 read(ir1,'(x,a10)',end=300) begin
      if(begin.eq.'ENERGY(eV)') goto 1
      goto 10
    1 i=i+1                                                             
      read(ir1,*,end=100) e(i),flux(i,1)                   
      goto 1                                                            
 100  nmax=i-1
      if(nmax.gt.100000) goto 200                                            
      ireads=1                                                          
      return                                                            
 200  write(6,201) nmax                                        
 201  format(1x,' the input data number is ',i5,' while the maximum
     1 dimension is 100000./','Please open the fortran file and exchange
     1 the e(100000),flux(100000,10)etc.'/,' to e(x),flux(x,10)etc.      
     1 all and re-compile')                              
      return
  300 write(6,*) 'Spectra data error: stop at ireads'
      stop
      end                                                               
c                                                                       
      subroutine pdata                                                  
c                                                                       
c --  prepare data for filter.                                          
c     called by main; call intf, sigc, sigr                             
c                                                                       
      implicit real*8 (a-h,o-z)                                         
      parameter (neof=100,njb=35,nkb=20)
      common/cross/sig,sigs(njb),bkl(njb,nkb)                              
      common/databk/eofph(neof),ebnd(njb),sigsub(njb,neof),                 
     *             bk(njb,neof,nkb),zz,xion,jp,ip,kp                       
      common/data/e(100000),flux(100000,10),nmax                           
      common/idata/zn,an,alp1,alp2,d,theta,den,aw,cont                  
      common/tdata/u(100000),apk(100000),temp(100000),uk,wk                   
c                                                                       
c  ----- check input data                                               
c                                                                       
      if(zz.ne.zn) goto 200                                             
c                                                                       
c --- cont=6.0221367d23*den/aw*1.d-24                                   
c                                                                       
      cont = 0.60221367*den/aw                                          
c                                                                       
c ---  change theta from degree into rad                                
c                                                                       
      theta=0.0174532 * theta                                           
c                                                                       
      do 1 i=1,nmax                                                     
      eof = e(i) / 1000.d0                                              
      call  intf(eof)                                                   
      sigc1 = sigc(eof)                                                 
      sigr1 = sigr(eof)                                                 
      sigt  = sig + sigr1 + sigc1                                       
      u(i)  = sigt * cont                                               
      apk(i)=( sigs(1) + 2.0 / zz * sigc1 ) / sigt                      
 1    continue                                                          
      wk =  ebnd(1) - ebnd(3)                                           
      call intf(wk)                                                     
      sigc1 = sigc(wk)                                                  
      sigr1 = sigr(wk)                                                  
      uk = (sig + sigr1 + sigc1 ) * cont                                
      wk = wk * 1000.0                                                  
      return                                                            
 200  write(6,201) zn,zz                                                
 201  format(1x,'the atomic number read from unit 5 is =',i5/           
     1 1x,'while the atomic number read from unit 2 is =',i5/           
     2 1x,'please check it')                                            
      stop                                                              
      end                                                               
c                                                                       
      function   ucoe(eof)                                              
c                                                                       
c ----- input: ephon : photon energy in kev                             
c ----- ouput: ucoe (cm-1)                                              
c      called by cbsf, ctsf; call intf, sigr, sigc.                     
c                                                                       
      implicit real*8 (a-h,o-z)                                         
      parameter (neof=100,njb=35,nkb=20)
      common/cross/sig,sigs(njb),bkl(njb,nkb)                              
      common/databk/eofph(neof),ebnd(njb),sigsub(njb,neof),                 
     *             bk(njb,neof,nkb),zz,xion,jp,ip,kp
      common/idata/zn,an,alp1,alp2,d,theta,den,aw,cont                  
      call intf(eof)                                                    
      ucoe=(sig+sigc(eof)+sigr(eof)) * cont                             
      return                                                            
      end                                                               
c                                                                       
      subroutine input(log)                                             
c                                                                       
c     read the database                                                 
c     here:                                                             
c       eofph      :   energy of photon energy in kev                   
c       sigtot     :   total cross in bar*eofph**3                      
c       ebnd       :   bending energy for each subshell in kev          
c       sigsub     :   subshell cross section in barns*eofph**3         
c       bk         :   angular distribution coeffecients                
c                                oct. 9, 1900. xiao-min tong            
c                                at riken                               
c                                                                       
      implicit real*8 (a-h,o-z)                                         
      parameter (neof=100,njb=35,nkb=20)
      common/databk/eofph(neof),ebnd(njb),sigsub(njb,neof),
     1             bk(njb,neof,nkb),zz,xion,jp,ip,kp                       
      data zero/0.d0/                                                   
c                                                                       
c     -------- initial all the array which will be used in the pro.     
c                                                                       
      do 1 i=1,neof
      eofph(i)=zero                                                     
      do 1 j=1,njb
      sigsub(j,i)=zero                                                  
      ebnd(j)=zero                                                      
      do 1 k=1,nkb
      bk(j,i,k)=zero                                                    
 1    continue                                                          
c                                                                       
c     ------------- read the database from the disk                     
c                                                                       
      read (log,789) zz,xion,jp,ip,kp                                   
      if(jp.gt.njb) stop 'jp is great than  35.'                         
      if(ip.gt.neof) stop 'ip is great than 100.'                        
      if(kp.gt.nkb) stop 'jp is great than  20.'                         
      read (log,788) (ebnd(j),j=1,jp),(eofph(i),i=1,ip),                
     *         ((sigsub(j,i),j=1,jp),i=1,ip),                           
     *         (((bk(j,i,k),j=1,jp),i=1,ip),k=1,kp)                     
 789  format(1x,2(f7.3,3x),3i10)                                        
 788  format(1x,6(1pd12.5,1x))                                          
      return                                                            
      end                                                               
c                                                                       
      subroutine intf(e)                                                
c                                                                       
c     calculate the cross section parameter at given energy e (kev)     
c     here:                                                             
c         sig    : total cross section   in barns                       
c         sigs   : subshell cross section in barns                      
c         bkl    : angular parameter                                    
c                                                                       
c
      implicit real*8 (a-h,o-z)                                         
      parameter (neof=100,njb=35,nkb=20)
      common/cross/sig,sigs(njb),bkl(njb,nkb)                              
      common/databk/eofph(neof),ebnd(njb),sigsub(njb,neof),                 
     *             bk(njb,neof,nkb),zz,xion,jp,ip,kp                       
c                                                                       
c   ------located the position                                          
c                                                                       
      sig=0.0                                                           
      do 200 i=1,njb                                                     
      sigs(i)=0.0                                                       
      do 200 j=1,nkb                                                     
      bkl(i,j)=0.0                                                      
 200  continue                                                          
      i=1                                                               
  1   if(e.ge.eofph(i).and.e.le.eofph(i+1)) goto 2                      
      i=i+1                                                             
      if(i.gt.ip) sig=sigsub(1,ip)/e**3                                 
      if(i.gt.ip) return                                                
      goto 1                                                            
  2   in=i                                                              
      if(e.ne.eofph(i)) goto 5                                          
      do 3 j=1,jp                                                       
      sigs(j)=sigsub(j,i)/e**3                                          
      do 3 k=1,kp                                                       
      bkl(j,k)=bk(j,i,k)                                                
  3   continue                                                          
      goto 101                                                          
  5   continue                                                          
      if(e.ne.eofph(i+1)) goto 6                                        
      i=i+1                                                             
      do 4 j=1,jp                                                       
      sigs(j)=sigsub(j,i)/e**3                                          
      do 4 k=1,kp                                                       
      bkl(j,k)=bk(j,i,k)                                                
  4   continue                                                          
      goto 101                                                          
  6   continue                                                          
      n=i+2                                                             
      aa=(e-eofph(n-1))*(e-eofph(n))                                    
      ab=(eofph(n-2)-eofph(n-1))*(eofph(n-2)-eofph(n))                  
      ba=(e-eofph(n-2))*(e-eofph(n))                                    
      bb=(eofph(n-1)-eofph(n))*(eofph(n-1)-eofph(n-2))                  
      ca=(e-eofph(n-1))*(e-eofph(n-2))                                  
      cb=(eofph(n)-eofph(n-1))*(eofph(n)-eofph(n-2))                    
      do 10 j=1,jp                                                      
      sigs(j)=                                                          
     *(aa/ab*sigsub(j,n-2)+ba/bb*sigsub(j,n-1)+ca/cb*sigsub(j,n))/e**3  
      do 10 k=1,kp                                                      
      bkl(j,k)=aa/ab*bk(j,n-2,k)+ba/bb*bk(j,n-1,k)+ca/cb*bk(j,n,k)      
 10   continue                                                          
 101  sig=0.0                                                           
      do 105 j=1,jp                                                     
      if(e.lt.ebnd(j)) goto 102                                         
      sig=sig+sigs(j)                                                   
      goto 105                                                          
 102  sigs(j)=0.0                                                       
      do 103 k=1,kp                                                     
      bkl(j,k)=0.0                                                      
 103  continue                                                          
 105  continue                                                          
      return                                                            
      end                                                               
c                                                                       
      function sigc(e)                                                  
c                                                                       
c -- compton cross section (bar); e (kev).                              
c                                                                       
      implicit real*8 (a-h,o-z)                                         
      parameter (neof=100,njb=35,nkb=20)
      common/databk/eofph(neof),ebnd(njb),sigsub(njb,neof),                 
     *             bk(njb,neof,nkb),zz,xion,jp,ip,kp                       
      r=e/511.0                                                         
      r2=2.0*(r+1.0)                                                    
      r21=2.0*r+1.0                                                     
      sig=3.0/8.0/r*((1.0-r2/r/r)*dlog(r21)+0.5+4.0/r-0.5/r21/r21)      
      sigc=sig*0.6651*zz                                                
      return                                                            
      end                                                               
c                                                                       
      function sigr(w)                                                  
c                                                                       
c --- rayleigh cross section (barn), w (kev).                           
c                                                                       
      implicit real*8 (a-h,o-z)                                         
      common/idata/zn,an,alp1,alp2,d,theta,den,aw,cont                  
      data sigt/0.124916d0/                                             
c --- sigt=r_0^2*pi/2.0                                                 
      al1=alp1*alp1                                                     
      al2=alp2*alp2                                                     
      x=(2.d0*w*1000.d0/27.2d0/137.d0)**2                               
      ak2=x/4.0                                                         
      ak4=ak2*ak2*4.0                                                   
      a2=an*an*al1*al1                                                  
      f1=a2*(x/al1/(al1+x)*(2.0+al1/ak2+al1*al1/ak4)                    
     1   -(1.0/ak2+2.0*al1/ak4)*dlog((al1+x)/al1)+1.0/ak2)              
      a2=(1.0-an)**2*al2*al2                                            
      f4=a2*(x/al2/(al2+x)*(2.0+al2/ak2+al2*al2/ak4)                    
     4   -(1.0/ak2+2.0*al2/ak4)*dlog((al2+x)/al2)+1.0/ak2)              
      p=2.0*dlog((al1+x)/al1*al2/(al2+x))                               
      p1=al1*dlog((al1+x)/al1)-dlog(((al2+x)/al2))*al2                  
      p2=al1**2*dlog((al1+x)/al1)-al2**2*dlog((al2+x)/al2)              
      p3=(al2-al1)+p1                                                   
      f2=2.0*an*(1.0-an)*al1*al2/(al2-al1)*(p+p3/ak2+p2/ak4)            
      f3=2.0*zn*an*al1/1837.0*((2.0+al1/ak2+al1*al1/ak4)*               
     3   dlog((al1+x)/al1)-2.0-al1/ak2)                                 
      f5=2.0*zn*(1.0-an)*al2/1837.0*((2.0+al2/ak2+al2*al2/ak4)*         
     5   dlog((al2+x)/al2)-2.0-al2/ak2)                                 
      f6=zn*zn/1837.0/1837.0*16.0/3.0*ak2                               
      f01=f1+f2+f3+f4+f5+f6                                             
      sigr=sigt*zn*zn/ak2*f01                                           
      return                                                            
      end                                                               
